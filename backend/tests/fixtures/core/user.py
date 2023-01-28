import pytest
from tests.factories.core.user import UserFactory


@pytest.fixture
def app_user_1():
    return UserFactory.create(
        email="colt@poliwag.com",
        phone='+18452428262',
        is_staff=False,
        is_active=True,
        user_profile__first_name="Colt",
        user_profile__last_name="Riess",
        user_profile__street_address='24 main street',
        user_profile__city='wallkill',
        user_profile__state='NY',
        user_profile__zipcode='12589',
        user_profile__birthday='1991-08-23',
        user_profile__citizenship_country_code='USA',
        user_profile__ssn='123456789',
    )
