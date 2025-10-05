from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message, Conversation
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related("sender", "receiver", "parent_message").prefetch_related("replies")
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            sender=self.request.user,
            receiver=self.request.data.get("receiver"),
            parent_message_id=self.request.data.get("parent_message")  # optional for replies
        )

    # ✅ Custom action to fetch conversations
    @action(detail=False, methods=["get"])
    def my_conversations(self, request):
        user = request.user
        # Message.objects.filter + select_related for optimization
        messages = Message.objects.filter(receiver=user).select_related("sender", "receiver", "parent_message")
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
