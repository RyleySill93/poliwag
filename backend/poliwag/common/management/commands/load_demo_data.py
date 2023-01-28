from os import environ

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line

from poliwag.common.database.backups.s3_restore import S3DatabaseBackupRestore


class Command(BaseCommand):
    help = "Loads data from production database"

    def handle(self, *args, **options):
        if settings.IS_PRODUCTION:
            raise Exception("STOP! You likely did not mean to do this on production...")

        environ["PGPASSWORD"] = settings.DATABASES['default']['PASSWORD']
        db_user = settings.DATABASES['default']['USER']
        drop_create_public_schema = (
            f"DROP SCHEMA IF EXISTS public CASCADE;"
            f" CREATE SCHEMA public;"
            f" GRANT ALL ON SCHEMA public TO {db_user};"
            f" GRANT ALL ON SCHEMA public TO public;"
        )

        execute_from_command_line(
            ["manage.py", "dbshell", "--", "-c", drop_create_public_schema]
        )
        S3DatabaseBackupRestore.restore_latest_backup()
        execute_from_command_line(["manage.py", "migrate"])
