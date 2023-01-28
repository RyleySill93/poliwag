import subprocess
import logging
from datetime import datetime
from os import path, environ, remove
from dataclasses import dataclass

from django.conf import settings


logger = logging.getLogger(__name__)


@dataclass
class PGDumpResult:
    filename: str
    output_path: str
    database: str

    def delete(self):
        remove(self.output_path)


class PGBackup:
    PG_DUMP = 'pg_dump -Fc --no-acl --no-owner -h %s -U %s %s > "%s"'
    PG_RESTORE = (
        "pg_restore -U {username} --clean --if-exists --no-acl --no-owner -v "
        '-j 8 -h {host} -p {port} -d {database_name} "{backup_file_path}"'
    )

    @classmethod
    def dump(cls, filename: str) -> PGDumpResult:
        database = 'default'
        database_host = settings.DATABASES[database]["HOST"]
        database_user = settings.DATABASES[database]["USER"]
        database_name = settings.DATABASES[database]["NAME"]
        environ["PGPASSWORD"] = settings.DATABASES[database]["PASSWORD"]
        output_path = path.join(settings.BASE_DIR, filename)
        cmd = cls.PG_DUMP % (database_host, database_user, database_name, output_path)

        try:
            logger.info("Starting backup of {} to {}".format(database_name, output_path))
            start = datetime.now()
            subprocess.run(
                cmd,
                shell=True,  # nosec
                check=True,  # Raise on failure
                timeout=(5 * 60),  # 5 minutes
                universal_newlines=True,  # Decode the output
                stderr=subprocess.PIPE,  # Capture stderr
            )
            end = datetime.now()
        except subprocess.TimeoutExpired as error:
            try:
                remove(output_path)
            except FileNotFoundError:
                pass

            logger.error("Backup of {} to {} timed out".format(database_name, output_path))
            raise error
        except subprocess.CalledProcessError as error:
            try:
                remove(output_path)
            except FileNotFoundError:
                pass

            logger.error(
                "Backup of {} to {} failed with code {}: {}".format(
                    database_name,
                    output_path,
                    error.returncode,
                    error.stderr,
                )
            )
            raise error
        else:
            logger.info(
                "Backup of {} to {} completed in {}".format(
                    database_name,
                    output_path,
                    (end - start),
                )
            )
            return PGDumpResult(filename, str(output_path), database=database_name)

    @classmethod
    def restore(cls, file_path: str):
        database = 'default'
        database_host = settings.DATABASES[database]["HOST"]
        database_port = settings.DATABASES[database]["PORT"]
        database_user = settings.DATABASES[database]["USER"]
        database_name = settings.DATABASES[database]["NAME"]

        cmd = cls.PG_RESTORE.format(
            username=database_user,
            host=database_host,
            port=database_port,
            database_name=database_name,
            backup_file_path=file_path,
        )

        try:
            logger.info("Restoring {} from {}".format(database, file_path))
            start = datetime.now()
            subprocess.run(
                cmd,
                shell=True,  # nosec
                executable="/bin/bash",
                stdout=None,
            )
            end = datetime.now()
        except subprocess.TimeoutExpired as error:
            logger.error("Restoring {} from {} timed out".format(database, file_path))
            raise error
        except subprocess.CalledProcessError as error:
            logger.error(
                "Restoring {} from {} failed with code {}: {}".format(
                    database,
                    file_path,
                    error.returncode,
                    error.stderr,
                )
            )
            raise error
        else:
            logger.info(
                "Restored {} from {} in {}".format(
                    database,
                    file_path,
                    (end - start),
                )
            )
