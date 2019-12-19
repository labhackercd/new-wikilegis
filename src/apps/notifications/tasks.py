from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from apps.notifications.models import (OwnerInvitation, PublicAuthorization,
                                       Notification)
from apps.notifications.emails import (send_owner_invitation,
                                       send_public_authorization,
                                       send_owner_closed_participation,
                                       send_feedback_participations)
from apps.participations.models import InvitedGroup, OpinionVote
from django.utils.translation import ugettext_lazy as _
from wikilegis import celery_app
from celery.utils.log import get_task_logger
from datetime import date, timedelta


logger = get_task_logger(__name__)


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


def closed_participation_notify(public_group):
    document = public_group.document
    notification = Notification()
    notification.user = document.owner
    if document.document_type and document.year and document.number:
        proposal_title = "%s %s/%s" % (document.document_type.initials,
                                       document.year, document.number)
    else:
        proposal_title = document.title
    message = 'A sua consulta pública sobre o proposição legislativa "{}"  \
               encontra-se encerrada'
    notification.message = message.format(proposal_title)
    notification.save()
    send_owner_closed_participation(public_group, proposal_title)


@celery_app.task
def participations_wait_feedback():
    yesterday = date.today() - timedelta(days=1)

    invited_groups = InvitedGroup.objects.filter(
        closing_date=yesterday,
        public_participation=True
    )

    users_emails = []

    for invited_group in invited_groups:

        suggestions = invited_group.suggestions.all()

        users_suggestions = suggestions.values_list('author__email', flat=True)

        suggestions_id = suggestions.values_list('id', flat=True)

        user_opnions = OpinionVote.objects.filter(id__in=suggestions_id)

        users_opnions = user_opnions.values_list('owner__email', flat=True)

        users_emails.extend(list(users_suggestions))
        users_emails.extend(list(users_opnions))

    users_emails = list(set(users_emails))

    for user_email in users_emails:
        send_feedback_participations(invited_group, user_email)

    return _(' Group {} participants were'
             'informed by email'.format(invited_group.document.title))
