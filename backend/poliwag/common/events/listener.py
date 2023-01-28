import abc
from .event import BaseEvent
from typing import List


class BaseListener(abc.ABC):
    """
    Meant to take actions when events happen.
    These actions should be anything but database writes:
        - read from the database
        - execute commands `BaseCommand`s which in turn invoke additional events
        - Do basic functions synchronously or asynchronously like send a notification
        Follow the pattern:
        When [event] occurs
        We shall [rules]
    """

    FOR_EVENTS: List[BaseEvent] = NotImplemented

    def __str__(self):
        return self.__class__.__name__

    @abc.abstractmethod
    def listen(self, event: BaseEvent):
        raise NotImplementedError

    @classmethod
    def build(cls, *args, **kwargs):
        return cls()
