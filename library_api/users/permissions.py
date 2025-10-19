from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Allows full access only to admin users.
    Read-only for others.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        # Allow GET, HEAD, OPTIONS for non-admins
        return request.method in permissions.SAFE_METHODS
