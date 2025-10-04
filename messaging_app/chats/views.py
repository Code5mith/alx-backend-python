from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Grab conversation_id from URL query params
        conversation_id = self.request.query_params.get("conversation_id")
        if not conversation_id:
            return Message.objects.none()  # no conversation_id => empty queryset

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Message.objects.none()

        # Check if user is a participant
        if self.request.user not in conversation.participants.all():
            # Explicitly return empty queryset to avoid unauthorized access
            return Message.objects.none()
        
        # Return messages only for this conversation
        return Message.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        conversation_id = self.request.data.get("conversation_id")
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(detail="Invalid conversation_id")

        # Check participant access
        if self.request.user not in conversation.participants.all():
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        serializer.save(sender=self.request.user, conversation=conversation)
