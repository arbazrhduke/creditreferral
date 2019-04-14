from rest_framework.permissions import BasePermission


class SuperUserPermission(BasePermission):
    """ A permission class that allows only a superuser to access the view."""
    def has_permission(self, request, view):
        return (request.user.is_superuser and request.method == 'GET') or request.method == 'POST'
