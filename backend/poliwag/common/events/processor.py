import abc
from collections import defaultdict
import logging
from typing import DefaultDict, List
import uuid

from poliwag import settings
from poliwag.common.utils import import_dotted_path_string
from .event import BaseEvent
from .listener import BaseListener


logger = logging.getLogger(__name__)


class BaseEventDAO(abc.ABC):
    def get(self, event_id: str):
        raise NotImplementedError

    def append(self, event: BaseEvent):
        raise NotImplementedError

    def remove(self, event: BaseEvent):
        raise NotImplementedError


from .models import AppEvent


class DjangoEventDao(BaseEventDAO):
    def get(self, id: uuid.UUID) -> BaseEvent:
        app_event = AppEvent.objects.get(pk=id)
        return BaseEvent.get_concrete_event_from_model(app_event)

    def append(self, event: BaseEvent) -> BaseEvent:
        data = event.to_dict()
        app_event = AppEvent.objects.create(**event.to_dict())
        return BaseEvent.get_concrete_event_from_model(app_event)

    def remove(self, event: BaseEvent) -> None:
        AppEvent.objects.get(id=event.id).delete()


class EventProcessor:
    """
    Handles all events.
        - Visits all projectors with events
        - Visits all listeners with events
    """

    def __init__(self, listener_registry: List[str], event_dao: BaseEventDAO):
        self.event_dao = event_dao

        self._listener_registry: DefaultDict[
            str, List[BaseListener]
        ] = self._register_listeners(listener_registry)

    def _register_listeners(
        self, listener_registry: List[str]
    ) -> DefaultDict[str, List[BaseListener]]:
        listener_registry_map = defaultdict(list)
        for listener in listener_registry:
            listener = import_dotted_path_string(listener)
            for event_class in listener.FOR_EVENTS:
                listener_registry_map[event_class.__name__].append(listener.build())

            logger.info(f"listener registered: {listener}")

        return listener_registry_map

    def process(self, event: BaseEvent):
        assert (
            len(self._listener_registry)
        ) > 0, "No listeners registered to EventProcessor!"
        self._handle_event(event)

    def _handle_event(self, event: BaseEvent):
        logger.info(f"handling event: {event}")
        if event.STORE_EVENT:
            self._store_event(event)

        self._run_listeners(event)

    def _validate_event(self, event) -> BaseEvent:
        return event.validate()

    def _run_listeners(self, event):
        listeners = self._listener_registry[event.__class__.__name__]
        for listener in listeners:
            logger.info(f"running listener: {listener.__class__.__name__}")
            listener.listen(event)

    def _store_event(self, event: BaseEvent):
        self.event_dao.append(event)

    def _remove_event(self, event: BaseEvent):
        self.event_dao.remove(event)


EP = EventProcessor(
    listener_registry=settings.EVENT_PROCESSING_LISTENER_REGISTRY,
    event_dao=DjangoEventDao(),
)
