from apps.notifications.models import ParcipantInvitation
from apps.notifications import emails
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Suggestion, InvitedGroup
from .clusters import clustering_suggestions
from constance import config
from datetime import date


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
    if suggestions.count() < config.MIN_SUGGESTIONS:
        clusters = [list(suggestions.values_list('id', flat=True))]
    else:
        clusters = str(clustering_suggestions(suggestions))
    group = InvitedGroup.objects.get(id=instance.invited_group.id)
    group.clusters = clusters
    group.save()


@receiver(post_save, sender=InvitedGroup)
def private_group_status(sender, instance, created, **kwargs):
    if created:
        if instance.public_participation:
            instance.group_status = 'waiting'
            instance.save()
        else:
            instance.openning_date = date.today()
            instance.save()
