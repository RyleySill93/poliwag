import operator
from boto3 import resource as boto3_resource
from botocore.config import Config
from decouple import config



class S3GenericStorage:
    def __init__(self):
        self.bucket_name = config('PROD_AWS_DB_BACKUPS_BUCKET_NAME')
        self.ACCESS_KEY = config('PROD_AWS_ACCESS_KEY_ID')
        self.SECRET_KEY = config('PROD_AWS_SECRET_ACCESS_KEY')

        if not self.bucket_name:
            raise Exception("Filesystem storage requires bucket name to be provided.")
        if not self.ACCESS_KEY:
            raise Exception(
                "Filesystem storage requires BACKUP_ACCESS_KEY "
                "to be defined in settings."
            )
        if not self.SECRET_KEY:
            raise Exception(
                "Filesystem storage requires BACKUP_SECRET_KEY "
                "to be defined in settings."
            )

    @property
    def bucket(self):
        s3 = boto3_resource(
            "s3",
            aws_access_key_id=self.ACCESS_KEY,
            aws_secret_access_key=self.SECRET_KEY,
            config=Config(signature_version="s3v4"),
        )

        return s3.Bucket(self.bucket_name)

    def write_file(self, name, path, acl=None):
        """ Write the specified file. """
        self.bucket.meta.client.upload_file(path, self.bucket.name, name)
        return self.get_file_url(self.get_latest_in_directory()[-1])

    def get_file_url(self, filepath):
        """ Returns URL for specified file """
        return self.bucket.meta.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket.name, "Key": filepath},
        )

    def delete_files(self, files):
        if files:
            for f in files:
                self.__delete_file_from_bucket(f)

    def __delete_file_from_bucket(self, key):
        self.bucket.meta.client.delete_object(
            Bucket=self.bucket.name,
            Key=key,
        )

    def list_directory(self, marker="", prefix="", min_file_size=None):
        """ List all stored files for the specified folder """
        files_list = self.bucket.objects.filter(Marker=marker, Prefix=prefix)
        files_dict = {}
        for file_ in files_list:
            # Skip files smaller than minimum
            if min_file_size and file_.size < min_file_size:
                continue
            files_dict[file_.last_modified] = file_.key

        return sorted(files_dict.items(), key=operator.itemgetter(0))

    def get_latest_in_directory(self, marker="", prefix=""):
        """ Returns last modified backup for specified folder """
        return self.list_directory(marker=marker, prefix=prefix)[-1]
