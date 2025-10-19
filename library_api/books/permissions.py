from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admin users can CRUD books.
    Regular users can only read.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        return request.method in permissions.SAFE_METHODS
