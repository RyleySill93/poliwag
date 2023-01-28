import logging
import uuid
from typing import Optional, Tuple
import requests
from io import BytesIO

from poliwag.settings import DOCUMENT_MOCK_STORAGE
from poliwag.common.utils import make_lazy
from poliwag.common.nanoid import NanoIdType
from poliwag.common.exceptions import InternalException
from poliwag.common.aws import S3Storage, MockS3Storage
from poliwag.common.nanoid import generate_custom_nanoid
from .models import Document
from .domains import DocumentDomain


logger = logging.getLogger(__name__)


class DocumentUploadFailed(InternalException):
    ...


class DocumentService:
    def __init__(self):
        # Avoid making a call to S3 on instantiation
        self.storage = make_lazy(self.get_storage_backend)

    def get_storage_backend(self):
        if DOCUMENT_MOCK_STORAGE:
            return MockS3Storage()

        return S3Storage()

    @classmethod
    def factory(cls) -> "DocumentService":
        return cls()

    def get_for_id(self, document_id: uuid.UUID) -> DocumentDomain:
        document = Document.objects.get(id=document_id)
        return DocumentDomain.from_model(document)

    def delete(self, document_id: uuid.UUID):
        document = Document.objects.get(pk=document_id)
        document.delete()

    def create_presigned_post(
        self,
        file_name: str,
        namespace: str,
        max_size: int = 100 * 1024 * 1024,  # 100MB
        uploaded_by_id: Optional[NanoIdType] = None,
        expiration: Optional[int] = 3600,
        is_public: bool = False,
    ) -> Tuple[DocumentDomain, str]:

        s3_key = self._make_s3_file_path(file_name, namespace, uploaded_by_id=uploaded_by_id)
        conditions = [
            ["content-length-range", 0, max_size],
        ]
        fields = {}

        if is_public:
            conditions.append({"acl": "public-read"})
            fields["acl"] = "public-read"

        post_url = self.storage.create_presigned_post(
            object_name=s3_key,
            expiration=expiration,
            conditions=conditions,
            fields=fields,
        )

        document_model = Document.objects.create(
            id=uuid.uuid4(),
            file_name=file_name,
            s3_key=s3_key,
            namespace=namespace,
            uploaded_by_id=uploaded_by_id,
            is_public=is_public,
        )

        document = self.get_for_id(document_model.id)

        return document, post_url

    def _make_s3_file_path(self, file_name: str, namespace: str, uploaded_by_id: Optional[str] = None) -> str:
        """
        Default entropy for files stored in s3
        :param file_name:
        :return:
        """
        uploaded_by = uploaded_by_id or 'system'
        # Prevent overwrites if we aren't using versioned S3
        increase_entropy = generate_custom_nanoid(size=6)
        return f"{uploaded_by}/{namespace}/{increase_entropy}-{file_name}"

    def upload(
        self,
        content: BytesIO,
        file_name: str,
        namespace: str,
        uploaded_by_id: Optional[NanoIdType] = None,
        is_public: bool = False,
    ) -> DocumentDomain:
        document, presigned_post = self.create_presigned_post(
            file_name=file_name,
            uploaded_by_id=uploaded_by_id,
            namespace=namespace,
            max_size=1000 * 1024 * 1024,  # 1GB
            is_public=is_public,
        )
        files = {"file": (file_name, content.read())}

        response = self.storage.upload_from_presigned_post(presigned_post, files)

        if response.status_code != 204:
            logger.error(response.text)
            raise DocumentUploadFailed(
                f"Failed to upload - Status: {response.status_code}"
            )

        logger.info(f"uploaded document key: {document.s3_key}")
        return document

    def get_signed_url_for_document_id(
        self,
        document_id: uuid.UUID,
        ttl_seconds: int = None,
        disposition: str = None,
        content_type: str = None,
    ) -> str:
        """
        Returns a signed url from the data store for the Document with no further permissions checks.
        :param document: The document
        :param ttl_seconds: The number of seconds the url is valid for. Default: 6 hours
        """
        document = Document.objects.get(pk=document_id)
        return self.storage.generate_presigned_url(
            document.s3_key,
            expires_in=ttl_seconds,
            disposition=disposition,
            content_type=content_type,
        )

    def upload_from_url(
        self,
        url: str,
        file_name: str,
        namespace: str,
        uploaded_by_id: Optional[NanoIdType] = None,
        is_public: bool = False,
    ) -> DocumentDomain:
        with requests.get(url, stream=True) as req_file:
            document = self.upload(
                content=BytesIO(req_file.content),
                file_name=file_name,
                uploaded_by_id=uploaded_by_id,
                namespace=namespace,
                is_public=is_public,
            )

        return document

    def delete_namespace(self, namespace: str):
        Document.objects.filter(namespace__startswith=namespace).delete()

        self.storage.delete_by_prefix(prefix=namespace)
