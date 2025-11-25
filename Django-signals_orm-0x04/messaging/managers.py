# ALX Task 4: Custom manager for unread messages

from django.db import models


class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Filter unread messages for a specific user.
        Optimized with .only().
        """
        return (
            super()
            .get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "sender", "receiver", "content", "timestamp")
        )
