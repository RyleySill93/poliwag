import ipdb
from django.db import IntegrityError
import logging
from typing import List
from poliwag.common.nanoid import NanoId, NanoIdType
from poliwag.common.exceptions import InternalException
from poliwag.common.identity.domains import IdentityDomain
from poliwag.common.identity.models import User
from poliwag.common.identity.events import UserRegistered, UserEventPayload


logger = logging.getLogger(__name__)


class IdentityAlreadyExists(InternalException):
    ...


class IdentityPhoneAlreadyExists(InternalException):
    ...


class IdentityEmailAlreadyExists(InternalException):
    ...


class IdentityService:
    @classmethod
    def factory(cls) -> "IdentityService":
        return cls()

    def bulk_create(self, users: List[IdentityDomain]):
        users = [
            User(
                id=user.id,
                phone=user.phone,
                email=user.email,
                is_active=user.is_active,
            )
            for user in users
        ]

        User.objects.bulk_create(users, ignore_conflicts=True)

    def bulk_update(self, users: List[IdentityDomain]):
        users = [
            User(
                id=user.id,
                phone=user.phone,
                email=user.email,
                is_active=user.is_active,
            )
            for user in users
        ]

        User.objects.bulk_update(
            users, fields=["first_name", "last_name", "email", "is_active"]
        )

    def create(self, user: IdentityDomain) -> IdentityDomain:
        # Validate integrity
        phone_exists = User.objects.filter(phone=user.phone).exists()
        email_exists = User.objects.filter(email=user.email).exists()
        if phone_exists and email_exists:
            raise IdentityAlreadyExists(f'Phone: {user.phone} Email: {user.email} already exist')

        elif phone_exists:
            raise IdentityPhoneAlreadyExists(f'Phone: {user.email} already exists')

        elif email_exists and not phone_exists:
            raise IdentityEmailAlreadyExists(f'Email: {user.email} already exists')

        # Create user
        user_obj = User.objects.create(
            id=user.id if user.id else NanoId.gen(),
            phone=user.phone,
            email=user.email,
        )

        # Emit event
        user_payload = UserEventPayload.from_model(user_obj)
        UserRegistered.new(payload=user_payload).emit()

        return self.get_by_id(user_obj.id)

    def update(self, user: IdentityDomain) -> IdentityDomain:
        # Update user
        User.objects.filter(id=user.id).update(
            phone=user.phone,
            email=user.email,
        )

        return self.get_by_id(user.id)

    def get_by_id(self, user_id: NanoIdType) -> IdentityDomain:
        user = User.objects.get(id=user_id)
        return IdentityDomain.from_model(user)

    def get_by_email(self, email: str) -> IdentityDomain:
        user = User.objects.get(email=email)
        return IdentityDomain.from_model(user)

    def get_by_phone(self, phone: str) -> IdentityDomain:
        user = User.objects.get(phone=phone)
        return IdentityDomain.from_model(user)

    def make_user_active(self, user_id: NanoIdType) -> IdentityDomain:
        User.objects.filter(id=user_id).update(is_active=True)
        return self.get_by_id(user_id=user_id)

    def list_by_ids(self, user_ids: List[NanoIdType]) -> List[IdentityDomain]:
        users = User.objects.filter(id__in=user_ids)
        return [IdentityDomain.from_model(user) for user in users]

    def list_by_emails(self, emails: List[str]) -> List[IdentityDomain]:
        users = User.objects.filter(email__in=emails)
        return [IdentityDomain.from_model(user) for user in users]
