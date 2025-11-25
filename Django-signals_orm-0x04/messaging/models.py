# ALX Task 4: Custom ORM Manager for unread messages with .only() optimization

from .managers import UnreadMessagesManager
from django.db import models
from django.contrib.auth.models import User


# ------------------------------------------
# CUSTOM MANAGER REQUIRED BY ALX
# ------------------------------------------
class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Returns unread messages for a specific user.
        Optimized with .only() to load minimal fields.
        """
        return (
            super()
            .get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "sender", "receiver", "content", "timestamp")
        )


# ------------------------------------------
# MESSAGE MODEL (includes read + parent_message + edited)
# ------------------------------------------
class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # Task 1 field
    edited = models.BooleanField(default=False)

    # Task 3: parent message for threaded replies
    parent_message = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies",
    )

    # Task 4: unread indicator
    read = models.BooleanField(default=False)

    # default + custom ORM managers
    objects = models.Manager()              # Django default
    unread = UnreadMessagesManager()        # ALX Task 4 manager

    def __str__(self):
        return f"Message {self.pk} from {self.sender} to {self.receiver}"

    # ------------------------------------------
    # Task 3: Recursive fetch of replies
    # ------------------------------------------
    def get_all_replies(self):
        all_replies = []

        def collect(node):
            children = node.replies.all()
            for child in children:
                all_replies.append(child)
                collect(child)

        collect(self)
        return all_replies

    @staticmethod
    def get_threaded_conversation(root_id):
        return (
            Message.objects
            .select_related("sender", "receiver", "parent_message")
            .prefetch_related("replies", "replies__replies")
            .get(pk=root_id)
        )


# ------------------------------------------
# MESSAGE HISTORY (Task 1 requirement)
# ------------------------------------------
class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="history"
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    # ALX requires this field
    edited_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"History of message {self.message_id} at {self.edited_at}"


# ------------------------------------------
# NOTIFICATIONS (Task 0)
# ------------------------------------------
class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="notifications"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user} about message {self.message_id}"
