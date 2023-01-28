import sys
import os

# Allows running specific pytest cases like backend/tests/unit
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poliwag.settings")
# Make celery always eager
os.environ.setdefault("CELERY_TASK_ALWAYS_EAGER", "True")
os.environ.setdefault("IS_TESTING", "RUNNING")
os.environ.setdefault("SLACK_MOCK_CLIENT", "True")
os.environ.setdefault("TWILIO_MOCK_CLIENT", "True")
os.environ.setdefault("DOCUMENT_MOCK_STORAGE", "True")


import django
django.setup()


import pytest

# Add fixtures here
pytest_plugins = [
    "tests.fixtures.core.user",
    "tests.fixtures.core.issuer",
    "tests.fixtures.core.investor",
]


@pytest.fixture(autouse=True)
def test_db(db):
    """
    Make the Django database available to all tests automatically
    """
    pass


@pytest.fixture(scope="session", autouse=True)
def sample_session_fixture(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        ...


@pytest.fixture
def staff_user(user_factory):
    return user_factory(
        email="dev@poliwag.com",
        password="password",
        first_name="Admin",
        last_name="poliwag",
        is_staff=True,
        is_active=True,
    )
