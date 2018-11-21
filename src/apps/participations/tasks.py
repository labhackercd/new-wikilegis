from apps.notifications import models, views


def save_invited_email(sender, instance, **kwargs):
    import ipdb; ipdb.set_trace()
    for participant in instance.thematic_group.participants.all():
        invited_email, created = models.InvitedEmail.objects.get_or_create(
            group=instance, email=participant.email)
        if created:
            views.send_invite(participant.email, instance.document.title,
                              invited_email.hash_id)
