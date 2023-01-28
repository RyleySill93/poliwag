from django.apps import AppConfig


class EventsConfig(AppConfig):
    name = "poliwag.common.events"

    def ready(self):
        from .processor import EP
