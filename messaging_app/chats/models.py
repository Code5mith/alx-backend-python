from django.db import models
from django_enum import EnumField
from django.db.models.functions import Now

# Create your models hereclass User(models.Model):
class User(models.Model):

    class RoleEnum(models.TextChoices):
        VALUE0 = "V0", "guest"
        VALUE1 = "V1", "host"
        VALUE2 = "V2", "admin"

    user_id = models.UUIDField(primary_key=True, auto_created=True)
    first_name  = models.CharField(null=False)
    last_name  = models.CharField(null=False)
    email = models.EmailField(_(""), unique=True, max_length=254, db_index=True)
    password_hash = models.CharField(null=False)
    phone_number = models.CharField(null=True)
    role = EnumField(RoleEnum, null=False, default=None)
    created_at = models.DateTimeField(db_default=Now())

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
