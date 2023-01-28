from slack_sdk.models.attachments import Attachment, AttachmentField
from poliwag import settings
from poliwag.common.events import BaseEvent, BaseListener
from poliwag.common.integrations.slack.service import SlackService


class EventSlackNotificationListener(BaseListener):
    FOR_EVENTS = []

    def listen(self, event: BaseEvent):
        GREEN = '#54D62C'
        service = SlackService()
        service.send_message(
            channel=settings.SLACK_EVENT_CHANNEL,
            text='',
            attachments=[
                Attachment(
                    text='',
                    color=GREEN,
                    pretext='User Event on poliwag Application',
                    title=event.event_type,
                    ts=event.created_at.timestamp(),
                    fields=[
                        AttachmentField(
                            title=key,
                            value=value,
                            short=True,
                        )
                        for key, value in event.payload.to_dict().items()
                    ],
                    footer='poliwag',
                    footer_icon='https://avatars.slack-edge.com/2022-06-15/3668451560822_8fa075d0092ceb9f190b_132.png',
                )
            ]
        )
