from rest_framework.views import APIView as _DRFAPIView
from rest_framework.response import Response
from poliwag.common.exceptions import APIException

# Helpful to have this next to views
APIException = APIException


class BaseAPIView(_DRFAPIView):
    ...


class PublicAPIView(_DRFAPIView):
    authentication_classes = ()
    permission_classes = ()


class APIStatusUrlView(PublicAPIView):
    def get(self, request):
        response = "💸 Ready to poliwag... 💸"

        return Response(response, content_type="text/html; charset=utf-8")
