from django.contrib.postgres.fields import JSONField
import json


class NonbinaryJSONField(JSONField):
    """
    The nonbinary json field should be used to
    store json payloads that aren't filtered on.
    This is because jsonb takes up significantly
    more disk space and is slower to write.
    """

    def db_type(self, connection):
        """
        Override to return `json` instead of jsonb
        """
        return "json"


class PureJSONField(NonbinaryJSONField):
    """
    Dont encode/decode the json values. Leave them as strings.
    """

    def to_python(self, value):
        return value

    def get_prep_value(self, value):
        return value

    def from_db_value(self, value, expression, connection):
        return json.dumps(value)
