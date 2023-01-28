from poliwag.common.nanoid import NanoIdType
from poliwag.common.identity.service import IdentityService


class PermissionService:
    def is_staff(self, user_id: NanoIdType) -> bool:
        user = IdentityService().get_by_id(user_id=user_id)
        return bool(user.is_staff)
