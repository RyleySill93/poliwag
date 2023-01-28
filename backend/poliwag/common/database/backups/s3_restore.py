import requests
import logging
import os
from dataclasses import dataclass

from django.conf import settings

from .pg import PGBackup
from .s3_storage import S3GenericStorage


logger = logging.getLogger(__name__)


@dataclass
class LatestBackupInfo:
    date: str

    @classmethod
    def factory(cls, path, date):
        return cls(date=date.isoformat())


class S3DatabaseBackupRestore:
    @classmethod
    def restore_latest_backup(cls):
        file_path = cls.download_latest_backup()
        try:
            PGBackup.restore(file_path)
        finally:
            os.remove(file_path)

    @staticmethod
    def download_latest_backup():
        engine = S3GenericStorage()

        try:
            _, last_backup_path = engine.get_latest_in_directory()
        except IndexError:
            raise Exception("There are no backups available.")

        url = engine.get_file_url(last_backup_path)
        logger.info(f"Found backup: {url}")

        logger.info("Downloading backup file...")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Will raise if request was not OK

        file_name = url.split("/")[-1].split("?")[0]
        file_path = os.path.join(settings.BASE_DIR, file_name)

        with open(file_path, "wb") as dump:
            for chunk in response.iter_content(chunk_size=4096):
                if chunk:
                    dump.write(chunk)
                    dump.flush()

        logger.info(f"Downloaded @ {file_path}")
        return file_path

    @staticmethod
    def get_latest_backup_info() -> LatestBackupInfo:
        engine = S3GenericStorage()

        try:
            date, last_backup_path = engine.get_latest_in_directory()
        except IndexError:
            raise Exception("There are no backups available.")

        return LatestBackupInfo.factory(last_backup_path, date)
