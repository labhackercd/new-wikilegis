from apps.notifications import models, emails


def save_invited_email(sender, instance, **kwargs):
    if instance.thematic_group:
        for participant in instance.thematic_group.participants.all():
            invitation, created = models.ParcipantInvitation.objects.get_or_create(
                group=instance, email=participant.email)
            if created:
                emails.send_participant_invitation(participant.email,
                                                   instance.document.title,
                                                   invitation.hash_id)
