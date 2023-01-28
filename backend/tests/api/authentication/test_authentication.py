import json

from django.db import transaction
from django.urls import reverse
from rest_framework import status
from poliwag.common.authentication.service import AuthenticationService


class TestAuthenticationEmail:
    """
    """
    def test_generate_authenticate_email(self, api_client, app_user_1):
        data = dict(email=app_user_1.email)
        url = reverse("gen-auth-email")
        response = api_client.post(url, data=json.dumps(data), content_type="application/json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_authenticate_email(self, api_client, app_user_1):
        service = AuthenticationService.factory()
        email_challenge_url = service.create_email_challenge(app_user_1.email)
        response = api_client.get(email_challenge_url)
        assert response.status_code == status.HTTP_302_FOUND

        # Ensure it can't be used again
        response = api_client.get(email_challenge_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_generate_authenticate_phone(self, api_client, app_user_1):
        data = dict(phone=app_user_1.phone)
        url = reverse("gen-auth-phone")
        response = api_client.post(url, data=json.dumps(data), content_type="application/json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_authenticate_phone(self, api_client, app_user_1):
        service = AuthenticationService.factory()
        auth_pc = service.create_phone_challenge(app_user_1.phone)
        url = reverse('auth-phone')
        response = api_client.post(url, data=dict(phone=app_user_1.phone, code=auth_pc.code))
        assert response.status_code == status.HTTP_200_OK

        with transaction.atomic():
            # Unusable after success
            url = reverse('auth-phone')
            response = api_client.post(url, data=dict(phone=app_user_1.phone, code=auth_pc.code))
            assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Wrong value
        auth_pc = service.create_phone_challenge(app_user_1.phone)
        url = reverse('auth-phone')
        response = api_client.post(url, data=dict(phone=app_user_1.phone, code=int(auth_pc.code) - 1))
        assert response.status_code == status.HTTP_400_BAD_REQUEST
