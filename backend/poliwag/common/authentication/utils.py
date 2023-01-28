from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from poliwag.common.utils import full_reverse
from poliwag.settings import APP_DOMAIN_NAME


def generate_auth_challenge_url(user):
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    return f"{APP_DOMAIN_NAME}/auth/email/{uidb64}/{token}/"
