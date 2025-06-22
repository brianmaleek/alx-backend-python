from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification for the receiver of the message
        notification_content = f"You have received a new message from {instance.sender.username}: {instance.content}"
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            content=notification_content
        )

@receiver(pre_save, sender=Message)
def save_before_edit(sender, instance, created, **kwargs):
    if instance.pk:
        # If the message is being edited, log the change
        original_message = Message.objects.get(pk=instance.pk)
        if original_message.content != instance.content:
            print(f"Message content changed from '{original_message.content}' to '{instance.content}'")
    else:
        print("Creating a new message.")

@receiver(post_delete, sender=User)
def delete_related_data(sender, instance, **kwargs):
    # Delete all messages and notifications related to the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    print(f"Deleted all messages and notifications for user {instance.username}.")