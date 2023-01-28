from rest_framework_simplejwt.tokens import RefreshToken
from poliwag.common.nanoid import NanoIdType
from poliwag.common.base_domains import BaseDomain
from poliwag.common.identity.domains import IdentityDomain


class UserAuthenticationDomain(BaseDomain):
    user_id: NanoIdType
    refresh: str
    access: str

    @classmethod
    def from_identity(cls, user: IdentityDomain) -> "UserAuthenticationDomain":
        # simple-jwt requires user instance which is why this is necessary
        from poliwag.common.identity.models import User
        user = User.objects.get(id=user.id)
        refresh = RefreshToken.for_user(user)

        return cls(
            user_id=user.id,
            refresh=str(refresh),
            access=str(refresh.access_token),
        )
