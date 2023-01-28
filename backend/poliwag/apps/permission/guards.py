from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from poliwag.common.exceptions import InternalException


_ = IsAuthenticated


class RequiredPermissionValueMissing(InternalException):
    ...


def _get_from_kwargs_or_request(request, field: str):
    value = request.kwargs.get(field)
    if not value:
        value = request.body.get(field)

    if not value:
        raise RequiredPermissionValueMissing(
            f"Missing required value for {field} in request body or kwargs"
        )

    return value


class IsStaffMember(BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.is_staff
