from typing import TypeVar

import pydantic

TEventPayload = TypeVar("TEventPayload", bound="BaseEventPayload")

_PAYLOAD_TYPE_REGISTRY = {}


class BaseEventPayload(pydantic.BaseModel):
    def __str__(self):
        return f"{type(self).__name__}"
