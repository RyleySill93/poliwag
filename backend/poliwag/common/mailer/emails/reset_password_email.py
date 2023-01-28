from .base_email import BaseEmail
from poliwag import settings


class ResetPasswordEmail(BaseEmail):
    from_email = f"no-reply@{settings.GENERIC_DOMAIN_NAME}"
    template_name = "reset-password.html"
    subject = f"Reset your {settings.COMPANY_NAME} password"
    required_context_variables = (
        "title",
        "reset_password_url",
    )
    base_context = {
        "title": "Reset your password",
    }
