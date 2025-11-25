# ALX Task 1: pre_save signal to log message edits

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification


# -------------------------------
# Task 0 (still needed)
# Notification when new message is created
# -------------------------------
@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


# -------------------------------
# Task 1
# Save old message content BEFORE update
# -------------------------------
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    If message is being edited (not newly created),
    save its old content to MessageHistory and mark edited=True
    """
    # If message does not exist yet → no edit happening
    if not instance.pk:
        return

    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # If the content changed → log history
    if old.content != instance.content:
        MessageHistory.objects.create(
            message=old,
            old_content=old.content
        )
        instance.edited = True


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
            edited_by=old.sender  # or set to instance.sender if preferred
        )
        instance.edited = True
