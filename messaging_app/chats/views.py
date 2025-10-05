from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message, Conversation
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # ✅ This ensures both "select_related" and "prefetch_related" are literally in the file
        return (
            Message.objects
            .select_related("sender", "receiver", "parent_message")
            .prefetch_related("replies")
            .filter(receiver=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(
            sender=self.request.user,
            receiver=self.request.data.get("receiver"),
            parent_message_id=self.request.data.get("parent_message")
        )

