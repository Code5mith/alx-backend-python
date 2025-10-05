from django.db import models
from django_enum import EnumField
from django.db.models.functions import Now
import uuid
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    A custom user model that extends Django's built-in AbstractUser.

    The AbstractUser model already includes fields like 'username', 'email',
    'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined',
    and all the necessary fields for authentication and permissions.

    We do not need to redefine fields that are already provided by AbstractUser.
    
    Any custom fields, such as a 'phone_number' or 'birth_date', should be
    added here.
    """
    class Role(models.TextChoices):
        GUEST = 'GUEST', 'Guest'
        MEMBER = 'MEMBER', 'Member'
        ADMIN = 'ADMIN', 'Administrator'

    phone_number = models.CharField(max_length=15, blank=True)
    password_hash = models.CharField(null=False)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.MEMBER,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Message(models.Model):
    message_id = models.UUIDField(_(""), primary_key=True)
    sender_id = models.ForeignKey(User, on_delete=models.PROTECT, to_field="user_id", related_name='equipment')
    message_body = models.TextField(_(""), null=False)
    sent_at = models.DateTimeField(db_default=Now())


class Conversation(models.Model):
    conversation_id = models.UUIDField(_(""), primary_key=True)
    participants_id = models.ForeignKey(User, on_delete=models.PROTECT, to_field="user_id", related_name='equipment')
    created_at = models.DateTimeField(db_default=Now())
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # Self-referential foreign key for replies (threaded conversations)
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:30]}"

    def get_all_replies(self):
        """
        Recursively fetch all replies to this message in threaded format.
        """
        all_replies = []
        for reply in self.replies.all():
            all_replies.append(reply)
            all_replies.extend(reply.get_all_replies())  # recursion
        return all_replies
