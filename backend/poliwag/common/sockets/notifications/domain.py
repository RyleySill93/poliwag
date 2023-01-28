import json
from dataclasses import dataclass
from .common import NotificationMessageTypes


@dataclass
class NotificationSocketMessageDomain:
    message: str
    data: dict

    def to_dict(self) -> dict:
        return {
            "type": NotificationMessageTypes.message,
            "data": json.loads(json.dumps(self.data, default=str)),
        }
