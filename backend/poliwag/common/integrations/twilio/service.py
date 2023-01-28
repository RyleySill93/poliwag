from types import SimpleNamespace
from twilio.rest import Client

from poliwag.common.integrations.twilio.utils import format_phone_number_e164
from poliwag import settings


class TwilioMockClient:
    """
    Used to mock slack events when we dont want to send them
    """
    class messages:
        @staticmethod
        def create(*args, **kwargs):
            return SimpleNamespace(sid='1234MockSMSMessage1234')


class TwilioService:
    def __init__(self):
        self.client = self.get_client()
        self.from_number = settings.TWILIO_PHONE_NUMBER

    @classmethod
    def factory(cls) -> "TwilioService":
        return cls()

    def get_client(self):
        if settings.TWILIO_MOCK_CLIENT:
            return TwilioMockClient()

        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN

        return Client(account_sid, auth_token)

    def send_sms_message(
        self,
        *,
        to_number: str,
        text: str,
    ) -> str:
        to_number = format_phone_number_e164(to_number)
        message = self.client.messages.create(
            body=text,
            from_=self.from_number,
            to=to_number,
        )

        return message.sid
