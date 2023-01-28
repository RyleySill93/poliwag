from django.conf import settings
from django.core.management.base import BaseCommand
from poliwag.common.database.backups.s3_upload import S3DatabaseBackupUploader


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not settings.IS_PRODUCTION:
            raise Exception("HALT! These backups are for production data only...")

        S3DatabaseBackupUploader.upload_new_backup()
