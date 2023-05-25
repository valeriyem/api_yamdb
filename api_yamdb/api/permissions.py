from rest_framework import permissions


class IsAuthorIsModeratorIsAdminIsSuperUser(permissions.BasePermission):
    """Анонимному пользователю доступны только безопасные запросы,
    автору объекта, модератору, админу, супрепользователю доуступны PATCH, DELETE."""

    def has_object_permission(self, request, view, obj):
        return(request.method in permissions.SAFE_METHODS
               or request.user.is_authenticated
               and (request.user == obj.author
                    or request.user.is_moderator
                    or request.user.is_admin
                    or request.user.is_superuser))