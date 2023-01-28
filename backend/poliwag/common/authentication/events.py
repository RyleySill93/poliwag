from poliwag.common.identity.events import UserEventPayload
from poliwag.common.events import BaseEvent


class UserAuthenticated(BaseEvent[UserEventPayload]):
    PAYLOAD_CLASS = UserEventPayload
