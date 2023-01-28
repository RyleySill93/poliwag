from rest_framework.response import Response

from poliwag.common.views import BaseAPIView
from poliwag.common.documents.service import DocumentService


class CreatePresignedUrlView(BaseAPIView):
    def post(self, request):
        file_directory_within_bucket = (
            f"user_upload_files/{request.user.id}/{request.data['filename']}"
        )
        document, presigned_post = DocumentService().create_presigned_post(
            file_name=file_directory_within_bucket,
            uploaded_by_id=request.user.id,
            namespace='user_upload'
        )

        return Response({"s3_headers": presigned_post, "url": document.url})


class DeleteDocumentView(BaseAPIView):
    def delete(self, request, **kwargs):
        DocumentService().delete(kwargs["document_id"])
        return Response()
