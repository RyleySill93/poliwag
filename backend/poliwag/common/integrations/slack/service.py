from typing import Optional, Sequence, Union, Dict

from slack_sdk.models.attachments import Attachment
from slack_sdk.models.blocks import Block
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from poliwag import settings


class SlackMockClient:
    """
    Used to mock slack events when we dont want to send them
    """

    def chat_postMessage(self, *args, **kwargs):
        ...


class SlackService:
    def __init__(self):
        self.client = self.get_slack_client()

    def get_slack_client(self):
        if settings.SLACK_MOCK_CLIENT:
            return SlackMockClient()

        return WebClient(token=settings.SLACK_BOT_TOKEN)

    def send_message(
        self,
        *,
        channel: str,
        text: Optional[str] = None,
        attachments: Optional[Sequence[Union[Dict[str, any], Attachment]]] = None,
        blocks: Optional[Sequence[Union[Dict[str, any], Block]]] = None,
        response_type: Optional[str] = None,
        replace_original: Optional[bool] = None,
        delete_original: Optional[bool] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.client.chat_postMessage(
            channel=channel,
            text=text,
            attachments=attachments,
            blocks=blocks,
            response_type=response_type,
            replace_original=replace_original,
            delete_original=delete_original,
            headers=headers,
        )
