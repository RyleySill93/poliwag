import pytest


@pytest.fixture
def patch_document_service(mocker):
    presigned_post = dict(
        url="https://poliwag-demo-documents.s3.bucket.com/blah",
        fields=["shouldnt-matter"],
    )
    mocker.patch(
        "poliwag.common.documents.service.S3Storage.create_presigned_post",
        return_value=presigned_post,
    )
    response = mocker.MagicMock()
    response.status_code = 204
    mocker.patch(
        "poliwag.common.documents.service.DocumentService._upload_from_presigned_post",
        return_value=response,
    )
