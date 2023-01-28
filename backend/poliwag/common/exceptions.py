from django.utils.translation import gettext_lazy
from rest_framework.views import exception_handler, set_rollback
from rest_framework.response import Response
from rest_framework.exceptions import APIException as _DRFApiException
from rest_framework import status
from typing import Dict, Optional


class InternalException(Exception):
    """
    All internal exceptions should inherit from this. We are handled
    vaguely publicly
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = gettext_lazy('Internal failure.')
    default_code = 'internal_failure'

    def __init__(self, message: str,  context: Optional[Dict] = None):
        self.message = message or self.default_detail
        self.context = context or dict()


class APIException(_DRFApiException):
    """
    API view layer exceptions
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = gettext_lazy('Invalid Request.')
    default_code = 'invalid_request'

    # Match the internal interface message
    def __init__(self, message=None, code=None):
        super().__init__(detail=message, code=code)


# Set in DRF config in settings.py and called by all API views
def api_exception_handler(exc, context):
    # Get DRF default handler response first
    response = exception_handler(exc, context)

    if isinstance(exc, InternalException):
        set_rollback()
        # We dont want to show the actual message here
        response = Response({}, status=exc.status_code)

    elif isinstance(exc, APIException):
        set_rollback()
        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}

        response = Response(data, status=exc.status_code)

    # If there is a response, it stemmed from type rest_framework.exceptions.APIException
    if response is not None:
        response.data['error'] = response.data.pop('detail', None)

    return response
