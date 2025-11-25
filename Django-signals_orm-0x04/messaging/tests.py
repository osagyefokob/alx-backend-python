from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class MessagingSignalsTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="pass")
        self.bob = User.objects.create_user(username="bob", password="pass")

    def test_post_save_creates_notification(self):
        msg = Message.objects.create(sender=self.alice, receiver=self.bob, content="Hello Bob")
        notifs = Notification.objects.filter(user=self.bob, message=msg)
        self.assertEqual(notifs.count(), 1, "Notification should be created when a message is created")

    def test_pre_save_saves_history_on_edit(self):
        msg = Message.objects.create(sender=self.alice, receiver=self.bob, content="First")
        msg.content = "Edited"
        msg.save()
        # After save, MessageHistory should have one record for that message
        histories = MessageHistory.objects.filter(message=msg)
        self.assertEqual(histories.count(), 1, "MessageHistory should record old content on edit")
        self.assertTrue(msg.edited, "Message.edited should be set to True after edit")
