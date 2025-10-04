from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Allows access only to objects owned by the requesting user.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
