from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from poliwag.common.views import BaseAPIView
from poliwag.core.user.service import UserService
from poliwag.core.user.domains import UserDomain


class GetCurrentUserView(BaseAPIView):
    def get(self, request):
        service = UserService.factory()
        user: UserDomain = service.get_by_id(request.user.id)
        return Response(data=user.to_dict(), status=status.HTTP_200_OK)


class PreviewCustomerIdFormView(BaseAPIView):
    def get(self, request):
        service = UserService.factory()
        forward_agreement = service.preview_customer_id_form(user_id=request.user.id)

        response = HttpResponse(
            forward_agreement,
            status=status.HTTP_200_OK,
            content_type='application/pdf'
        )
        response['Content-Disposition'] = 'inline'

        return response
