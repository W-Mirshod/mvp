from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models.jwt import BlackListedAccessToken


class IsTokenValid(permissions.BasePermission):
    """
    Custom permission to check if the provided JWT is valid.
    """
    def has_permission(self, request, view):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return False
        try:
            jti, jti_refresh = token.split()
            blacklisted_token = BlackListedAccessToken.objects.filter(jti=jti, jti_refresh=jti_refresh).first()
            if blacklisted_token:
                raise PermissionDenied('Access token is blacklisted')
            return True
        except Exception:
            return False

class IsOneTimeTokenValid(permissions.BasePermission):
    """
    Custom permission to check if the provided one-time JWT is valid.
    """
    def has_permission(self, request, view):
        try:
            token = request.headers.get('Authorization').split()[1]
            RefreshToken(token).validate(request.user, one_time=True)
        except Exception as e:
            raise PermissionDenied(detail="Invalid or expired one-time token.")
        return True

class IsOwner(permissions.BasePermission):
    """
    Custom permission to check if the user is the owner of the object.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
