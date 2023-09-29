from rest_framework import permissions


class AdminCreateUpdateDestroyPermission(permissions.BasePermission):
    """
    Custom permission to only allow admin users to create, update or delete an object and allow any user to list and retrieve.
    """

    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.is_superuser
        return True
