from apps.notifications.models import ParcipantInvitation
from apps.notifications import emails
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Suggestion, InvitedGroup
from .clusters import clustering_suggestions


def save_invited_email(sender, instance, **kwargs):
    if instance.thematic_group:
        for participant in instance.thematic_group.participants.all():
            invitation, created = ParcipantInvitation.objects.get_or_create(
                group=instance, email=participant.email)
            if created:
                emails.send_participant_invitation(participant.email,
                                                   instance.document.title,
                                                   invitation.hash_id)


@receiver(post_save, sender=Suggestion)
def clustering_group(sender, instance, **kwargs):
    suggestions = Suggestion.objects.filter(
        invited_group=instance.invited_group)
    group = InvitedGroup.objects.get(id=instance.invited_group.id)
    group.clusters = str(clustering_suggestions(suggestions))
    group.save()
