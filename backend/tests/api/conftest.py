import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client_user_authenticated(app_user):
    client = APIClient()
    client.force_login(user=app_user)
    return client

@pytest.fixture
def api_client():
    client = APIClient()
    return client
