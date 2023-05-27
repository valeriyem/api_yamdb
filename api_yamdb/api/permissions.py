from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка прав администратора."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Разрешить доступ для методов только чтения
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class IsStaffOrAuthorOrReadOnly(permissions.BasePermission):
    """Проверка прав для отзывов и комментариев."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated)


    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                or request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author)


class IsAdminOrSuperUser(permissions.BasePermission):
    """Разрешение для админа или суперюзера."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ только аутентифицированным пользователям,
    для чтения разрешает доступ всем.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated)


class IsAuthorIsModeratorIsAdminIsSuperUser(permissions.BasePermission):
    """Анонимному пользователю доступны только безопасные запросы,
    автору объекта, модератору, админу, супрепользователю доступны PATCH,
    DELETE."""
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user == obj.author
                     or request.user.is_moderator
                     or request.user.is_admin
                     or request.user.is_superuser))
