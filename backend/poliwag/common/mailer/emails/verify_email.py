from .base_email import BaseEmail
from poliwag.settings import COMPANY_NAME, GENERIC_DOMAIN_NAME


class VerifyEmail(BaseEmail):
    from_email = f"no-reply@{GENERIC_DOMAIN_NAME}"
    template_name = "confirm-email.html"
    subject = f"Verify your email to start using {COMPANY_NAME}"
    required_context_variables = ("title", "product", "verification_url")
    base_context = {
        "title": "Verify your email",
        "product": COMPANY_NAME,
    }
