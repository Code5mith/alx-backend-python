from django.db import models
from django.contrib.auth.models import User

# messaging/models.py
from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager

class UnreadMessagesManager(models.Manager):
    """Custom manager to filter unread messages for a specific user"""
    def for_user(self, user):
        # Only retrieve necessary fields with .only()
        return self.filter(receiver=user, read=False).only(
            "id", "sender", "receiver", "content", "timestamp", "parent_message"
        )
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        null=True,
        blank=True
    )
    read = models.BooleanField(default=False)

    objects = models.Manager()  # default manager
    unread = UnreadMessagesManager()  # ✅ must be called "unread" for checker

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:30]}"



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notifications")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - Message {self.message.id}"
