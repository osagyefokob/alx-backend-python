from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class MessagingTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')

    def test_message_creation_creates_notification(self):
        msg = Message.objects.create(sender=self.user1, receiver=self.user2, content='Hello')
        self.assertEqual(Notification.objects.filter(user=self.user2, message=msg).count(), 1)

    def test_message_edit_creates_history(self):
        msg = Message.objects.create(sender=self.user1, receiver=self.user2, content='Hello')
        msg.content = 'Hello edited'
        msg.save()
        self.assertTrue(msg.edited)
        self.assertEqual(msg.history.count(), 1)
