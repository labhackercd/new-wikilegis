from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from apps.notifications.models import OwnerInvitation, PublicAuthorization
from apps.notifications.emails import (send_owner_invitation,
                                       send_public_authorization)


@receiver(post_save, sender=OwnerInvitation)
def save_owner_invitation(sender, instance, **kwargs):
    user, created = User.objects.get_or_create(email=instance.email)
    user.profile.profile_type = 'owner'
    user.profile.save()
    send_owner_invitation(instance.email)


@receiver(post_save, sender=PublicAuthorization)
def save_public_authorization(sender, instance, created, update_fields,
                              **kwargs):
    if instance.closing_date:
        send_public_authorization(instance, True)
    else:
        send_public_authorization(instance)
