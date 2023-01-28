from .base_email import BaseEmail
from poliwag.settings import COMPANY_NAME


class WelcomeEmail(BaseEmail):
    from_email = "from@example.com"
    template_name = "welcome.html"
    subject = f"Welcome to {COMPANY_NAME}!"
    required_context_variables = ("title", "product", "name")
    base_context = {
        "title": f"Welcome to {COMPANY_NAME}!",
        "product": COMPANY_NAME,
    }
