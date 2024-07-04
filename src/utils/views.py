from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from apps.users.serializers import UserSerializer
from .permissions import IsTokenValid, IsOwner
from apps.users.models import User

class MultiSerializerViewSet(ModelViewSet):
    filtersets = {
        "default": None,
    }
    serializers = {
        "default": Serializer,
    }

    @property
    def filterset_class(self):
        return self.filtersets.get(self.action) or self.filtersets.get("default")

    @property
    def serializer_class(self):
        return self.serializers.get(self.action) or self.serializers.get("default", Serializer)

    def get_response(self, data=None):
        return Response(data)

    def get_valid_data(self, many=False):
        serializer = self.get_serializer(data=self.request.data, many=many)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None

        paginator = self.paginator
        if "ordering_fields" in self.__dict__:
            paginator.sorted_by = self.ordering_fields
        return paginator.get_paginated_response(data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsTokenValid, IsOwner]

    def get_object(self):
        obj = super().get_object()
        if not self.request.user.is_superuser and obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to access this object.")
        return obj