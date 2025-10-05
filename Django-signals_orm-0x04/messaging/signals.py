# messaging/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
# messaging/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    Notification.objects.filter(user=instance).delete()

