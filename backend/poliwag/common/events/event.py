import datetime
from django.db import transaction
import uuid
from typing import Optional, TypeVar, Generic
from poliwag.common.nanoid import NanoIdType

from .payload import BaseEventPayload, _PAYLOAD_TYPE_REGISTRY


_EVENT_TYPES_REGISTRY = {}


class BaseEventMeta(type):
    """
    Metaclass to register event classes and create version to schema map
    """

    def __new__(mcs, name, bases, attrs):
        klass = super().__new__(mcs, name, bases, attrs)
        _EVENT_TYPES_REGISTRY[klass.__name__] = klass

        if klass.PAYLOAD_CLASS != NotImplemented and issubclass(
            klass.PAYLOAD_CLASS, BaseEventPayload
        ):
            _PAYLOAD_TYPE_REGISTRY[klass.PAYLOAD_CLASS.__name__] = klass.PAYLOAD_CLASS

        return klass


TPayload = TypeVar("TPayload", bound=BaseEventPayload)


class BaseEvent(Generic[TPayload], metaclass=BaseEventMeta):
    """
    unique event id
    event type: name of the class containing event data
    aggregate type: name of the aggregate's class IE `Fund`
    aggregate id: id of aggregate
    data: serialized event data, e.g. JSON
    created: timestamp at which the event happened
    user id: optional id of the user or other actor which triggered the event
    tx id: group events triggered in the same contract
    """

    PAYLOAD_CLASS = NotImplemented
    # If you dont want to store an event in the DB, set this to False
    STORE_EVENT: bool = True

    __slots__ = [
        "id",
        "event_type",
        "_payload",
        "_payload_class",
        "user_id",
        "created_at",
    ]

    def __str__(self):
        return f"<{self.event_type}> id: {self.id}"

    def __repr__(self):
        return str(self)

    def __init__(
        self,
        id: uuid.UUID,
        event_type: str,
        payload: TPayload,
        user_id: Optional[str] = None,
        created_at: Optional[datetime.datetime] = None,
    ):
        self.id = id
        self.event_type = event_type
        self._payload = payload
        self._payload_class = self.PAYLOAD_CLASS.__name__

        # Event meta
        self.created_at = created_at or datetime.datetime.now()
        self.user_id = user_id

    @property
    def payload(self) -> TPayload:
        return self._payload

    @classmethod
    def new(
        cls,
        payload: TPayload,
        user_id: Optional[NanoIdType] = None,
    ):
        return cls(
            id=uuid.uuid4(),
            event_type=cls.__name__,
            payload=payload,
            user_id=user_id,
        )

    def emit(self):
        from .processor import EP

        EP.process(self)
        # @TODO Process after transaction commits
        # transaction.on_commit(lambda: EP.process(self))

    @classmethod
    def get_concrete_event_from_model(cls, event) -> "BaseEvent":
        """
        Returns the correct concrete event given model object
        """
        klass = _EVENT_TYPES_REGISTRY[event.event_type]
        payload_class = _PAYLOAD_TYPE_REGISTRY[event.payload_class]
        payload = payload_class(**event.payload)

        return klass(
            id=event.id,
            event_type=event.event_type,
            payload=payload,
            user_id=event.user_id,
            created_at=event.created_at,
        )

    @classmethod
    def get_concrete_event_from_dict(cls, event) -> "BaseEvent":
        """
        Returns the correct concrete event given raw event data as a dict
        """
        klass = _EVENT_TYPES_REGISTRY[event["event_type"]]
        payload_class = _PAYLOAD_TYPE_REGISTRY[event["payload_class"]]
        payload = payload_class(**event.payload)

        return klass(
            id=event["id"],
            event_type=event["event_type"],
            payload=payload,
            user_id=event["user_id"],
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "event_type": self.event_type,
            "payload": self.payload.to_dict(),
            "payload_class": self._payload_class,
            "user_id": self.user_id,
        }
