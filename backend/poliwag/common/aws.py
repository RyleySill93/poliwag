from types import SimpleNamespace
import logging
import boto3
from botocore.exceptions import ClientError
import requests
from poliwag import settings
from poliwag.common.utils import split_every


logger = logging.getLogger(__name__)


class EC2Explorer:
    def __init__(self):
        self.client = self._get_client()

    def _get_client(self):
        return boto3.client(
            "ec2",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME,
        )

    def describe_instances(self):
        return self.client.describe_instances()


class CloudFrontExplorer:
    def __init__(self):
        self.client = self._get_client()

    def _get_client(self):
        return boto3.client(
            "cloudfront",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME,
        )

    def describe_instances(self):
        return self.client.list_distributions()


class S3Storage:
    def __init__(self):
        self.client = self._get_client()

    def _get_client(self):
        client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME,
        )

        return client

    @classmethod
    def get_url_for_key(cls, object_name: str):
        from storages.backends.s3boto3 import S3Boto3Storage

        return S3Boto3Storage().url(object_name)

    def delete_by_prefix(self, prefix: str):
        paginator = self.client.get_paginator("list_objects_v2")
        response = paginator.paginate(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Prefix=prefix,
            MaxKeys=1000,
        )
        objects_to_delete = []
        for page in response:
            if "Contents" in page:
                objects_to_delete.extend(page["Contents"])

        S3_MAX_DELETE_SIZE = 1000
        for chunk in split_every(objects_to_delete, S3_MAX_DELETE_SIZE):
            self.client.delete_objects(
                Delete={"Objects": [{"Key": s3_object["Key"]} for s3_object in chunk]},
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            )
            logger.info(f"deleted {len(chunk)} objects with prefix: {prefix}")

    def create_presigned_put(self, object_name, expiration=3600):
        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        # Generate a presigned URL for the S3 object
        try:
            response = self.client.generate_presigned_url(
                "put_object",
                Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": object_name},
                ExpiresIn=expiration,
            )
        except ClientError as e:
            logging.error(e)
            return None

        # The response contains the presigned URL
        return response

    def create_presigned_post(
        self, object_name, fields=None, conditions=None, expiration=3600
    ):
        """Generate a presigned URL S3 POST request to upload a file

        :param bucket_name: string
        :param object_name: string
        :param fields: Dictionary of prefilled form fields
        :param conditions: List of conditions to include in the policy
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Dictionary with the following keys:
            url: URL to post to
            fields: Dictionary of form fields and values to submit with the POST
        :return: None if error.
        """
        try:
            response = self.client.generate_presigned_post(
                settings.AWS_STORAGE_BUCKET_NAME,
                object_name,
                Fields=fields,
                Conditions=conditions,
                ExpiresIn=expiration,
            )
        except ClientError as e:
            logging.error(e)
            return None

        # The response contains the presigned URL and required fields
        return response

    def generate_presigned_url(
        self,
        filename: str,
        expires_in: int = None,
        disposition: str = None,
        content_type: str = None,
    ) -> str:
        """
        Returns a signed url from the data store for the the object with no further permissions checks.
        :param filename: The full filename and path (Key) for this object in the Bucket.
        :param expires_in: The number of seconds the url is valid for. Default: 6 hours
        :return:
        """
        if expires_in is None:
            expires_in = 6 * 60 * 60  # 6 hours

        params = {
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "Key": filename,
        }

        if disposition:
            params["ResponseContentDisposition"] = disposition

        if content_type:
            params["ResponseContentType"] = content_type

        url = self.client.generate_presigned_url(
            "get_object",
            Params=params,
            ExpiresIn=expires_in,
        )

        return url

    def upload_from_presigned_post(self, presigned_post, files):
        response = requests.post(
            presigned_post["url"], files=files, data=presigned_post["fields"]
        )
        return response


class MockS3Storage:
    """
    Used to prevent tests from generating documents
    """
    @classmethod
    def get_url_for_key(cls, object_name: str):
        return f'offline-file-store/{object_name}'

    def delete_by_prefix(self, prefix: str):
        pass

    def create_presigned_put(self, object_name, expiration=3600):
        return {
            'url': f'offline-file-store/{object_name}',
            'fields': {
                'key': object_name,
                'AWSAccessKeyId': settings.AWS_ACCESS_KEY_ID,
                'policy': 'eyJleHBpcmF0aW9uIjogIjIwMjItMDctMThUMTY6MDg6MzJaIiwgImNvbmRpdGlvbnMiOiBbWyJjb250ZW50LWxlbmd0aC1yYW5nZSIsIDAsIDEwNDg1NzYwMDBdLCB7ImJ1Y2tldCI6ICJ0YXAtc2FuZGJveC1kb2N1bWVudHMifSwgeyJrZXkiOiAidzkvb2NoUUEyLVc5LWNvbHQtcmllc3MtMjAyMi0wNy0xOFQxNTowODozMi45NjA0OTVaLnBkZiJ9XX0=',
                'signature': 'wIrg8qsnvk2O79U629qTkCJf7LQ='
            }
        }

    def create_presigned_post(
        self, object_name, fields=None, conditions=None, expiration=3600
    ):
        return {
            'url': f'offline-file-store/{object_name}',
            'fields': {
                'key': object_name,
                'AWSAccessKeyId': settings.AWS_ACCESS_KEY_ID,
                'policy': 'eyJleHBpcmF0aW9uIjogIjIwMjItMDctMThUMTY6MDg6MzJaIiwgImNvbmRpdGlvbnMiOiBbWyJjb250ZW50LWxlbmd0aC1yYW5nZSIsIDAsIDEwNDg1NzYwMDBdLCB7ImJ1Y2tldCI6ICJ0YXAtc2FuZGJveC1kb2N1bWVudHMifSwgeyJrZXkiOiAidzkvb2NoUUEyLVc5LWNvbHQtcmllc3MtMjAyMi0wNy0xOFQxNTowODozMi45NjA0OTVaLnBkZiJ9XX0=',
                'signature': 'wIrg8qsnvk2O79U629qTkCJf7LQ='
            }
        }

    def generate_presigned_url(
        self,
        filename: str,
        expires_in: int = None,
        disposition: str = None,
        content_type: str = None,
    ) -> str:
        return f'offline-file-store/{filename}'

    def upload_from_presigned_post(self, presigned_post, files):
        response = SimpleNamespace(text='', status_code=204)
        return response
