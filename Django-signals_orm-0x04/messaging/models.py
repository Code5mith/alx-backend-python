from django.db import models
from django.contrib.auth.models import User

# messaging/models.py
from django.db import models
from django.contrib.auth.models import User
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
    read = models.BooleanField(default=False)  # read/unread status

    objects = models.Manager()  # default manager
    unread_messages = UnreadMessagesManager()  # ✅ custom manager

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:30]}"

    def get_all_replies(self):
        all_replies = []
        for reply in self.replies.all():
            all_replies.append(reply)
            all_replies.extend(reply.get_all_replies())
        return all_replies


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notifications")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - Message {self.message.id}"
