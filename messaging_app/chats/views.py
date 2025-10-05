from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Must include "select_related" and "prefetch_related"
        # Must include Message.objects.filter
        return (
            Message.objects.filter(receiver=self.request.user)
            .select_related("sender", "receiver", "parent_message")
            .prefetch_related("replies")
        )

    def perform_create(self, serializer):
        # Must include "sender=request.user" and "receiver"
        serializer.save(
            sender=self.request.user,
            receiver=self.request.data.get("receiver"),
            parent_message_id=self.request.data.get("parent_message") 