import logging
import random
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from poliwag.common.nanoid import NanoId, NanoIdType
from poliwag.common.exceptions import InternalException
from poliwag.common.identity.service import IdentityService
from poliwag.common.authentication.domains import UserAuthenticationDomain
from poliwag.common.authentication.models import AuthPhoneChallenge
from poliwag.common.mailer.emails.auth_challenge_email import AuthChallengeEmail
from poliwag.common.integrations.twilio.service import TwilioService
from poliwag.common.authentication.utils import generate_auth_challenge_url


logger = logging.getLogger(__name__)


class AuthChallengeFailed(InternalException):
    ...


class AuthChallengeCodeIncorrect(AuthChallengeFailed):
    """
    Use when the code doesnt match the expected value
    """
    ...


class AuthChallengeExpired(AuthChallengeFailed):
    """
    Use when the challenge is expired
    """
    ...


class AuthChallengeTooManyAttempts(AuthChallengeFailed):
    """
    Use when the user has tried too many times
    """
    ...


class AuthenticationService:
    MAX_ATTEMPTS = 3

    def __init__(self, identity_service: IdentityService, sms_service: TwilioService):
        self._identity_service = identity_service
        self._sms_service = sms_service

    @classmethod
    def factory(cls) -> "AuthenticationService":
        return cls(
            identity_service=IdentityService.factory(),
            sms_service=TwilioService.factory()
        )

    def create_email_challenge(self, email) -> str:
        # @TODO the hash formula uses User we can change later
        # user = self._identity_service.get_by_email(email)
        from poliwag.common.identity.models import User
        user = User.objects.get(email=email)
        url = generate_auth_challenge_url(user)
        AuthChallengeEmail.send(recipients=[user.email], context={"auth_challenge_url": url})
        
        return url

    def auth_user_email_challenge(self, user_id, token) -> UserAuthenticationDomain:
        # @TODO the hash formula uses User we can change later
        # user = self._identity_service.get_by_email(email)
        from poliwag.common.identity.models import User
        user = User.objects.get(id=user_id)

        if default_token_generator.check_token(user, token):
            if not user.is_active:
                user = self._identity_service.make_user_active(user_id=user_id)

            return UserAuthenticationDomain.from_identity(user)

        raise AuthChallengeFailed('invalid token')

    def create_phone_challenge(self, phone: str) -> AuthPhoneChallenge:
        user = self._identity_service.get_by_phone(phone=phone)
        self._deactivate_previous_attempts_for_user(user.id)

        auth_pc = AuthPhoneChallenge(
            id=NanoId.gen(),
            user_id=user.id,
            code=self._generate_challenge_code(),
            is_active=True,
            expires_at=timezone.now() + timezone.timedelta(minutes=5)
        )
        auth_pc.save()

        # Only send if contract succeeds
        sms_send = lambda: self._sms_service.send_sms_message(
            to_number=user.phone,
            text=f'{auth_pc.code} is your poliwag authentication code.\n@poliwag.com #{auth_pc.code}'
        )
        transaction.on_commit(sms_send)

        return auth_pc

    def _deactivate_previous_attempts_for_user(self, user_id: NanoIdType):
        deactivated_count = (
            AuthPhoneChallenge.objects
            .filter(user_id=user_id).update(is_active=False)
        )
        logger.info(f'{deactivated_count} challenges deactivated')

    def _generate_challenge_code(self, length: int=6) -> str:
        min = pow(10, length - 1)
        max = pow(10, length) - 1
        return str(random.randint(min, max))

    def auth_user_phone_challenge(self, user_id: NanoIdType, code: str) -> UserAuthenticationDomain:
        user = self._identity_service.get_by_id(user_id=user_id)
        auth_pc = AuthPhoneChallenge.objects.get(user_id=user_id, is_active=True)
        auth_pc.num_attempts += 1
        auth_pc.save()

        if auth_pc.num_attempts > self.MAX_ATTEMPTS:
            self.create_phone_challenge(user.phone)
            raise AuthChallengeTooManyAttempts('Too many attempts')

        is_expired = timezone.now() > auth_pc.expires_at
        if is_expired:
            self.create_phone_challenge(user.phone)
            raise AuthChallengeExpired('Expired challenge')

        is_correct = auth_pc.code == int(code)
        if is_correct:
            if not user.is_active:
                user = self._identity_service.make_user_active(user_id=user_id)
            # Make this obsolete
            AuthPhoneChallenge.objects.filter(user_id=user_id).update(is_active=False)

            user_auth_domain = UserAuthenticationDomain.from_identity(user)
            return user_auth_domain
        else:
            raise AuthChallengeCodeIncorrect('Incorrect challenge')

    def flush_expired_tokens(self):
        # Delete any blacklisted tokens which should be run periodically
        from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
        from rest_framework_simplejwt.utils import aware_utcnow
        OutstandingToken.objects.filter(expires_at__lte=aware_utcnow()).delete()
