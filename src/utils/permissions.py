from django.db import transaction
from rest_framework import permissions
from rest_framework_simplejwt.exceptions import InvalidToken

from src.apps.users.models.jwt import BlackListedAccessToken
from src.apps.users.serializers import RestorePasswordSerializer


class IsTokenValid(permissions.BasePermission):
    """
    Custom permission to check if the provided JWT is valid.
    """

    def has_permission(self, request, view):

        if request.user.is_one_time_jwt_created:
            return False

        if not request.auth:
            return False

        is_allowed_user = not BlackListedAccessToken.objects.filter(
            user=request.user.id, token=request.auth.token.decode("utf-8")
        ).exists()
        if not is_allowed_user:
            raise InvalidToken("Token is blacklisted")

        return True


class IsOneTimeTokenValid(permissions.BasePermission):
    """
    Custom permission to check if the provided one-time JWT is valid.
    """

    def has_permission(self, request, view):

        is_allowed_user = not BlackListedAccessToken.objects.filter(
            user=request.user.id, token=request.auth.token.decode("utf-8")
        ).exists()
        if not is_allowed_user:
            raise InvalidToken("Token is blacklisted")

        request.data["user_id"] = request.user.id
        serializer = RestorePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_one_time_jwt_created:
            request.user.is_one_time_jwt_created = False
            try:
                with transaction.atomic():
                    BlackListedAccessToken.objects.create(
                        jti=request.auth.payload.get("jti"),
                        jti_refresh=f'access_{request.auth.payload.get("jti")}',
                        token=request.auth,
                        user=request.user,
                    )
                    request.user.save()
            except Exception as e:
                request.user.is_one_time_jwt_created = False
                request.user.save()
                raise InvalidToken(f"The token cannot be blacklisted: {e}")

        return True


class IsOwner(permissions.BasePermission):
    """
    Custom permission to check if the user is the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        # check for the default user model and object owner field
        return obj.owner == request.user
