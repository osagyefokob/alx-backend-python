# ALX Task 3: Threaded conversations using parent_message and ORM optimization

from django.db import models
from django.contrib.auth.models import User


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

    # Task 3: threaded replies
    parent_message = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies",
    )

    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message {self.pk} from {self.sender} to {self.receiver}"

    # ---------------------------------------------
    # TASK 3:
    # Optimized query for threaded conversations
    # ---------------------------------------------
    @staticmethod
    def get_threaded_conversation(root_message_id):
        """
        Returns a root message with all nested replies using select_related and prefetch_related.
        """

        # Load the root message with sender/receiver optimized
        root = (
            Message.objects
            .select_related("sender", "receiver", "parent_message")
            .prefetch_related("replies", "replies__replies")
            .get(pk=root_message_id)
        )

        return root

    # ---------------------------------------------
