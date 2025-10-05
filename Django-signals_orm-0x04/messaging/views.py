from django.shortcuts import render

# Create your views here.
# messaging/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer

# messaging/views.py
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)\
                              .select_related("sender", "receiver", "parent_message")\
                              .prefetch_related("replies")

    @method_decorator(cache_page(60))  # ✅ cache timeout: 60 seconds
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class UnreadMessageViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        # ✅ Use the custom manager
        unread_messages = Message.unread_messages.for_user(user).select_related("sender", "receiver", "parent_message")
        serializer = MessageSerializer(unread_messages, many=True)
        return Response(serializer.data)
