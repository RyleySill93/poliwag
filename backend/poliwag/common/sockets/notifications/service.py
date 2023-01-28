from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from poliwag.common.nanoid import NanoIdType
from poliwag.common.sockets.notifications.common import NotificationGroupKey
from poliwag.common.sockets.notifications.domain import NotificationSocketMessageDomain


class NotificationSocketService:
    """
    Use to push/receive data to sockets outside consumer context
    """

    def __init__(self):
        self.channel_layer = get_channel_layer()

    def broadcast_message_for_account_id(
        self, user_id: NanoIdType, message: NotificationSocketMessageDomain
    ):
        key = NotificationGroupKey.get(user_id)
        async_to_sync(self.channel_layer.group_send)(
            group=key,
            message=message.to_dict(),
        )
