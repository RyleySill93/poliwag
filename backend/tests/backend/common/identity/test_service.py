from poliwag.common.nanoid import NanoId
from poliwag.common.identity.service import IdentityService
from poliwag.common.identity.domains import IdentityDomain


class TestIdentityService:
    def test_create_user(self):
        """
        Ensure we can create a new identity object
        """
        user_domain = IdentityDomain(
            id=NanoId.gen(),
            email="dev@poliwag.com",
            phone='55555555555',
        )
        user = IdentityService().create(user=user_domain)

        assert user.id
