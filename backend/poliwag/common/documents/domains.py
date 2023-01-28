import uuid
from datetime import datetime
from typing import Optional

from poliwag.common.nanoid import NanoIdType
from poliwag.settings import AWS_STORAGE_BUCKET_NAME
from poliwag.common.aws import S3Storage
from poliwag.common.base_domains import BaseDomain


class DocumentDomain(BaseDomain):
    id: uuid.UUID
    namespace: Optional[str] = None
    file_name: Optional[str] = None
    s3_key: Optional[str] = None
    uploaded_by_id: Optional[NanoIdType] = None
    uploaded_datetime: Optional[datetime] = None
    is_public: Optional[bool] = None

    @property
    def url(self) -> str:
        if self.is_public:
            return (
                f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{self.s3_key}"
            )
        else:
            return S3Storage.get_url_for_key(self.s3_key)

    @classmethod
    def from_model(cls, model_instance) -> "DocumentDomain":
        if not model_instance:
            return None

        return cls(
            id=model_instance.id,
            uploaded_by_id=model_instance.uploaded_by_id,
            file_name=model_instance.file_name,
            namespace=model_instance.namespace,
            s3_key=model_instance.s3_key,
            is_public=model_instance.is_public,
            uploaded_datetime=model_instance.created_at,
        )
