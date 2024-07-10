from rest_framework import permissions
from rest_framework_simplejwt.exceptions import InvalidToken

from apps.users.models.jwt import BlackListedAccessToken


class IsTokenValid(permissions.BasePermission):
    """
    Custom permission to check if the provided JWT is valid.
    """

    def has_permission(self, request, view):
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
        return True


class IsOwner(permissions.BasePermission):
    """
    Custom permission to check if the user is the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        # check for the default user model and object owner field
        return obj.owner == request.user
