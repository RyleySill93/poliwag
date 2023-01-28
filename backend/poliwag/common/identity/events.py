from pydantic import EmailStr
from poliwag.common.nanoid import NanoIdType
from poliwag.common.identity.models import User
from poliwag.common.events import BaseEvent, BaseEventPayload


class UserEventPayload(BaseEventPayload):
    user_id: NanoIdType
    email: EmailStr
    first_name: str
    last_name: str

    @classmethod
    def from_model(cls, user: User):
        return cls(
            user_id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )

    def to_dict(self):
        return {
            "user_id": str(self.user_id),
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }


class UserActivated(BaseEvent[UserEventPayload]):
    PAYLOAD_CLASS = UserEventPayload


class UserRegistered(BaseEvent[UserEventPayload]):
    PAYLOAD_CLASS = UserEventPayload
