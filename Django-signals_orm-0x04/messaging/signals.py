# ALX Task 2: Cleanup user-related data after account deletion

from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


# -----------------------------------
# TASK 0 + TASK 1 SIGNALS REMAIN
# -----------------------------------

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old.content != instance.content:
        MessageHistory.objects.create(
            message=old,
            old_content=old.content,
            edited_by=old.sender
        )
        instance.edited = True


# -----------------------------------
# TASK 2 — post_delete on USER
# -----------------------------------
@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    When a user is deleted:
    - Delete all messages they sent
    - Delete all messages they received
    - Delete all notifications addressed to them
    - Delete history entries connected to their messages
    """

    # Delete messages where user was sender or receiver
    user_messages = Message.objects.filter(sender=instance) | Message.objects.filter(receiver=instance)

    # Delete all message histories linked to those messages
    MessageHistory.objects.filter(message__in=user_messages).delete()

    # Delete notifications for this user
    Notification.objects.filter(user=instance).delete()

    # Finally delete the messages themselves
    user_messages.delete()
