import json
import logging
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from poliwag.common.sockets.notifications.common import NotificationGroupKey


logger = logging.getLogger(__name__)


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        try:
            user = self.scope["user"]
        except KeyError:
            return

        if user.is_authenticated:
            self._add_connection_to_user_group(user)
            self.accept()

    def _add_connection_to_user_group(self, user):
        key = NotificationGroupKey.get(user_id=user.id)
        async_to_sync(self.channel_layer.group_add)(key, self.channel_name)

    def disconnect(self, close_code):
        try:
            user = self.scope["user"]
        except KeyError:
            return

        self._remove_connection_from_user_group(user)

    def _remove_connection_from_user_group(self, user):
        key = NotificationGroupKey.get(user_id=user.id)
        async_to_sync(self.channel_layer.group_discard)(key, self.channel_name)

    def notification_message(self, message: dict):
        """
        Handles messages with type: `notification.message`
        """
        raw = json.dumps(message)
        self.send(raw)

    def receive(self, text_data):
        print("inside message receive")
