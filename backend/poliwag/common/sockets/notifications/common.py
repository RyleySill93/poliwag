from poliwag.common.nanoid import NanoIdType


class NotificationMessageTypes:
    message = "notification.message"


class NotificationGroupKey:
    """
    We want all connections from a user grouped together. For example
    what if they are using poliwag in multiple browser tabs?
    """

    GROUP_KEY = "notifications"

    @classmethod
    def get(cls, user_id: NanoIdType):
        return f"{cls.GROUP_KEY}-{user_id}"
