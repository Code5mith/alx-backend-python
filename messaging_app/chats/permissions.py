from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission: only allow users to access their own objects.
    """

    def has_object_permission(self, request, view, obj):
        # Assuming your model has a `user` field (FK to the owner)
        return obj.user == request.user
