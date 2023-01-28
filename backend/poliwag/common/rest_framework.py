from rest_framework import viewsets
from rest_framework import pagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.transaction import non_atomic_requests as _non_atomic_request
from django.utils.decorators import method_decorator


# Use to make a view ignore default ATOMIC_REQUEST behavior
non_atomic_view = method_decorator(_non_atomic_request, name="dispatch")


class AggregateView(APIView):
    """
    The base class for AggregateView
        An AggregateView is a view which is used to dispatch the requests to the appropriate views
        This is done so that we can use one URL with different methods (GET, PUT, etc)
    """

    def dispatch(self, request, *args, **kwargs):
        method = request.method.lower()
        if hasattr(self, method):
            return getattr(self, method).as_view()(request, *args, **kwargs)

        return JsonResponse(
            {
                "error": f"{request.method} not implemented for {self.__class__.__name__}"
            },
            status=405,
        )


class ActionAttributes:
    permission_classes = None
    queryset = None
    serializer_class = None

    def get_permissions(self, view):
        if self.permission_classes is None:
            raise NotImplementedError("Permissions not implemented")

        return self.permission_classes

    def get_queryset(self, view):  # todo set view as context instead of arg
        if self.queryset is None:
            raise NotImplementedError("Queryset not implemented")

        return self.queryset

    def get_serializer_class(self, view):
        if self.serializer_class is None:
            raise NotImplementedError("Serializer not implemented")

        return self.serializer_class


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


# Allows you to customize serializers, permissions, and querysets per action
class tapViewSet(viewsets.ModelViewSet):
    create_attributes = None
    retrieve_attributes = None
    list_attributes = None
    update_attributes = None
    partial_update_attributes = None
    destroy_attributes = None

    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    def _get_method_attributes(self):
        method_attributes_by_action = dict(
            create=self.create_attributes,
            retrieve=self.retrieve_attributes,
            list=self.list_attributes,
            update=self.update_attributes,
            partial_update=self.partial_update_attributes,
            destroy=self.destroy_attributes,
        )

        if self.action not in method_attributes_by_action:
            raise ValueError(f"Unrecognized action: {self.action}")

        attributes = method_attributes_by_action[self.action]

        if attributes is None:
            raise NotImplementedError(
                f"Method attributes not implemented for: {self.action}"
            )

        return attributes()

    def get_permissions(self):
        attributes = self._get_method_attributes()
        permissions = attributes.get_permissions(self)
        return [permission() for permission in permissions]

    def get_queryset(self):
        attributes = self._get_method_attributes()
        return attributes.get_queryset(self)

    def get_serializer_class(self):
        attributes = self._get_method_attributes()
        return attributes.get_serializer_class(self)
