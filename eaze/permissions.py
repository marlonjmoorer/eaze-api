from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsListOrIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            if request.method in SAFE_METHODS:
                return True
        else:
            return True

class IsCreationOrIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            if view.action == 'create':
                return True
            else:
                return False
        else:
            return True