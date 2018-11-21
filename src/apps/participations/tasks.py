from apps.notifications import models, emails


def save_invited_email(sender, instance, **kwargs):
    for participant in instance.thematic_group.participants.all():
        invited_email, created = models.ParcipantInvitation.objects.get_or_create(
            group=instance, email=participant.email)
        if created:
            emails.send_invite(participant.email, instance.document.title,
                               invited_email.hash_id)
