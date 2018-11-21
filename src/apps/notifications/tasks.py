from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.notifications.models import OwnerInvitation
from apps.notifications.emails import send_owner_invitation


@receiver(post_save, sender=OwnerInvitation)
def save_owner_invitation(sender, instance, **kwargs):
    send_owner_invitation(instance.email, instance.hash_id)
