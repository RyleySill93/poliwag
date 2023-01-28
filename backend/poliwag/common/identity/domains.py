import datetime
from typing import Optional
from rest_framework_simplejwt.tokens import RefreshToken

from poliwag.common.nanoid import NanoIdType
from poliwag.common.base_domains import BaseDomain
from poliwag.common.identity.models import User


class IdentityDomain(BaseDomain):
    id: Optional[NanoIdType]
    email: str
    phone: str
    is_active: Optional[bool] = False
    is_staff: Optional[bool] = False

    @classmethod
    def from_model(cls, model_instance: User) -> "IdentityDomain":
        if not model_instance:
            return None

        return cls(
            id=model_instance.id,
            email=model_instance.email,
            phone=model_instance.phone,
            is_active=model_instance.is_active,
            is_staff=model_instance.is_staff,
        )
