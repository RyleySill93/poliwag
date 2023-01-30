from .base_email import BaseEmail
from poliwag.settings import COMPANY_NAME, GENERIC_DOMAIN_NAME


class AuthChallengeEmail(BaseEmail):
    from_email = f"no-reply@{GENERIC_DOMAIN_NAME}"
    template_name = "auth-email-challenge.html"
    subject = f"OldLogin to poliwag"
    required_context_variables = ("title", "auth_challenge_url")
    base_context = {
        "title": "OldLogin to poliwag",
    }
