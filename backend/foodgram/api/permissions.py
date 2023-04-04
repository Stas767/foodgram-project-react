from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Изменение, удаление и создание разрешено только автору."""

    def has_object_permission(self, request, view, obj):
        if obj.author != request.user and request.method not in SAFE_METHODS:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        return super().has_object_permission(request, view, obj)
