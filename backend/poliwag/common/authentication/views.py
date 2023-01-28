from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlsafe_base64_decode
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from poliwag.common.rest_framework import non_atomic_view
from poliwag.common.views import PublicAPIView, APIException
from poliwag.common.utils import parse_phone_number, slugify_phone_number
from poliwag.settings import APP_DOMAIN_NAME
from poliwag.common.authentication.service import (
    AuthenticationService,
    AuthChallengeFailed,
    AuthChallengeExpired,
    AuthChallengeTooManyAttempts,
    AuthChallengeCodeIncorrect,
)


TokenRefreshView = TokenRefreshView


class GenerateEmailAuthView(PublicAPIView):
    def post(self, request):
        User = get_user_model()
        email = request.data["email"]
        try:
            auth_service = AuthenticationService.factory()
            auth_service.create_email_challenge(email)
        except User.DoesNotExist:
            raise APIException(message=f'No user found for email {email}')

        return Response(status=status.HTTP_201_CREATED)


class AuthenticateEmailView(PublicAPIView):
    def get(self, request, uidb64, token):
        try:
            User = get_user_model()
            user_id = urlsafe_base64_decode(uidb64).decode("utf-8")
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise APIException(message='No user found')

        try:
            # Auth
            auth_service = AuthenticationService.factory()
            user_auth_domain = auth_service.auth_user_email_challenge(user_id=user_id, token=token)
        except AuthChallengeFailed:
            raise APIException(message=f'Invalid link for authentication')

        # Ensure token can't be reused
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        response = HttpResponseRedirect(f"{APP_DOMAIN_NAME}/login")
        response.set_cookie("jwt", user_auth_domain.access)
        return response



class GeneratePhoneAuthView(PublicAPIView):
    def post(self, request):
        phone_input = request.data['phone']
        User = get_user_model()
        try:
            phone = slugify_phone_number(phone_input)
        except ValueError:
            raise APIException(message=f"Not a valid phone {phone_input}.")

        try:
            user = User.objects.get(phone=phone)
        except ObjectDoesNotExist:
            raise APIException(message=f"No user found with phone {phone}.")

        auth_service = AuthenticationService.factory()
        challenge = auth_service.create_phone_challenge(phone)
        return Response(
            data={'user_id': user.id, 'challenge_id': challenge.id},
            status=status.HTTP_201_CREATED,
        )

@non_atomic_view
class AuthenticatePhoneView(PublicAPIView):
    def post(self, request):
        User = get_user_model()
        phone = slugify_phone_number(request.data['phone'])
        code = request.data['code']

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise APIException(message=f"No user found with phone {phone}.")

        auth_service = AuthenticationService.factory()
        try:
            user_auth_domain = auth_service.auth_user_phone_challenge(user_id=user.id, code=code)
        except ObjectDoesNotExist:
            raise APIException(message="No active code.")
        except AuthChallengeCodeIncorrect:
            raise APIException(message="Code incorrect please try again")
        except AuthChallengeExpired:
            raise APIException(message="Code expired, new code sent")
        except AuthChallengeTooManyAttempts:
            raise APIException(message="Too many attempts, new code sent")

        response = Response(
            status=status.HTTP_200_OK,
            data={
                "access": user_auth_domain.access,
                "refresh": user_auth_domain.refresh,
            },
        )
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        return response
