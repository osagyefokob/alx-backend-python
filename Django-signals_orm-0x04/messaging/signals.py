from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    """
    When a new Message is created, create a Notification for the receiver.
    """
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def save_message_history_on_edit(sender, instance, **kwargs):
    """
    Before a Message is saved, if it already exists and its content changed,
    save the old content in MessageHistory and mark message as edited.
    """
    if not instance.pk:
        # New message, nothing to compare
        return

    try:
        old = Message.objects.get(pk=instance.pk)
    except ObjectDoesNotExist:
        return

    if old.content != instance.content:
        # save old content to history before the change
        MessageHistory.objects.create(message=old, old_content=old.content)

        # mark the instance as edited so that field reflects later
        instance.edited = True

@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    """
    When a user is deleted, remove messages, notifications and histories
    related to the user. Using cascade ensures DB integrity but we remove
    explicitly to make intent clear.
    """
    # Delete messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications for the user
    Notification.objects.filter(user=instance).delete()
