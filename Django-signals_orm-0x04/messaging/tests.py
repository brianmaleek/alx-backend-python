from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

# Create your tests here.
class MessageNotificationTests(TestCase):
    def setUp(self):
        # Create users
        self.sender = User.objects.create_user(username='sender', password='password')
        self.receiver = User.objects.create_user(username='receiver', password='password')

    def test_message_creation(self):
        # Ensure no messages exist before creating one
        self.assertEqual(Message.objects.count(), 0)

        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello, this is a test message!')

        # Check if the message is created correctly
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.sender, self.sender)
        self.assertEqual(message.receiver, self.receiver)
        self.assertEqual(message.content, 'Hello, this is a test message!')
        self.assertIsNotNone(message.timestamp)


    def test_notification_creation(self):
        # Ensure no notifications exist before creating a message
        self.assertEqual(Notification.objects.count(), 0)

        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Test Message!')

        # Check if the message is created correctly
        notification = Notification.objects.filter(
            user=self.receiver,
            message=message).exists()

        self.assertIsNotNone(notification)
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        self.assertEqual(notification.read)
