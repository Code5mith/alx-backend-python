from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to view, send, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Only authenticated users can access the API at all
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Ensure the requesting user is part of the conversation.
        Assumes:
          - Message model has a `conversation` FK
          - Conversation model has a `participants` ManyToMany field
        """
        return request.user in obj.conversation.participants.all()
