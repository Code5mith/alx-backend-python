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
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            sender=self.request.user,
            receiver=self.request.data.get("receiver"),
            parent_message_id=self.request.data.get("parent_message")
        )

    def list(self, request, *args, **kwargs):
        # ✅ Explicitly include both "Message.objects.filter" and "select_related"
        messages = Message.objects.filter(receiver=request.user).select_related("sender", "receiver", "parent_message")
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

