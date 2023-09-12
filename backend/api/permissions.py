from django.conf import settings
from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsAuthor(BasePermission):
    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)
    

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return (
                request.user.is_superuser
                or request.user.role == settings.USER_ADMIN
            )
        return False


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            # or (request.user.is_authenticated
            #     and request.user.is_superuser
            #     or request.user.role == settings.USER_ADMIN)
        )
