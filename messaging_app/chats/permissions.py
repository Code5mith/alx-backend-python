from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Only allow authenticated participants of a conversation
    to view, send, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Only authenticated users can access the API at all
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Only allow participants of the conversation to:
        - view messages (GET, HEAD, OPTIONS)
        - send messages (POST)
        - update messages (PUT, PATCH)
        - delete messages (DELETE)
        """
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return request.user in obj.conversation.participants.all()

        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return request.user in obj.conversation.participants.all()

        # Default deny
        return False
