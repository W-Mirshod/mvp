from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken


class IsTokenValid(permissions.BasePermission):
    """
    Custom permission to check if the provided JWT is valid.
    """

    def has_permission(self, request, view):
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            return False
        try:
            jti, jti_refresh = token.split()
            refresh_token = RefreshToken(jti_refresh)
            refresh_token.verify()
            return True
        except Exception:
            return False


class RefreshToken(RefreshToken):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_one_time = kwargs.get("is_one_time", False)


class IsOneTimeTokenValid(permissions.BasePermission):
    """
    Custom permission to check if the provided one-time JWT is valid.
    """

    def has_permission(self, request, view):
        try:
            token = request.headers.get("Authorization").split()[1]
            refresh_token = RefreshToken(token)
            refresh_token.verify()
            if refresh_token.payload.get("one_time", False):
                return True
            else:
                raise PermissionDenied("Token is not one-time")
        except Exception:
            raise PermissionDenied(detail="Invalid or expired one-time token.")
        return False


class IsOwner(permissions.BasePermission):
    """
    Custom permission to check if the user is the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
