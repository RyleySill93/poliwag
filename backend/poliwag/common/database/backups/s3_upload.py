import logging
from datetime import datetime

from django.conf import settings

from .s3_storage import S3GenericStorage
from .pg import PGBackup, PGDumpResult


logger = logging.getLogger(__name__)


class S3DatabaseBackupUploader:
    @classmethod
    def upload_new_backup(cls):
        file_name = cls._get_file_name()
        pg_dump = PGBackup.dump(file_name)
        cls._upload_to_bucket(pg_dump)

    @classmethod
    def _get_file_name(cls):
        return "backup.{:%Y-%m-%d-%H-%M-%S}.dump".format(
            datetime.now(),
        )

    @classmethod
    def _upload_to_bucket(cls, pg_dump: PGDumpResult):
        logger.info(f"Uploading ({pg_dump.filename}) to S3...")
        engine = S3GenericStorage()
        url = engine.write_file(pg_dump.filename, pg_dump.output_path)
        logger.info(f"File saved @ {url}")
        logger.info(f"Removing backup file ({pg_dump.filename})...")
        pg_dump.delete()
