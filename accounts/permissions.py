from rest_framework.permissions import BasePermission

from accounts.models import Account


class IsAdmin(BasePermission):
    message = "Admin access is required."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == Account.Role.ADMIN
        )


class IsAdminOrModerator(BasePermission):
    message = "Admin or moderator access is required."

    def has_permission(self, request, view):
        allowed_roles = {
            Account.Role.ADMIN,
            Account.Role.MODERATOR,
        }

        return (
            request.user.is_authenticated
            and request.user.role in allowed_roles
        )
