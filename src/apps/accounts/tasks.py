from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    UserProfile.objects.get_or_create(user=instance)
