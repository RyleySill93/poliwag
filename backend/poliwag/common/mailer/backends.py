import os
from django.conf import settings
from django.core.mail.backends.filebased import EmailBackend


class EmailToBrowserBackend(EmailBackend):
    """
    Stores emails locally at specified
    Forwards emails to browser window instead of actually sending them
    """

    def close(self):
        r = super().close()
        if settings.DEBUG and not os.environ.get("IS_TESTING", False):
            import webbrowser

            file_name = self._get_filename()
            full_file_path = f"{settings.DEV_EMAIL_FILE_PATH}{file_name}"
            webbrowser.open(full_file_path)
        return r

    def _get_filename(self):
        """
        file://C:/Users/Andrew/dev/poliwag/backend/tmp/email/20200711-195800-140616466503216.html
        """
        fname = super()._get_filename()
        fname, ext = os.path.splitext(fname)
        return f"{fname}.html"
