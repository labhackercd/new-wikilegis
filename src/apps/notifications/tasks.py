from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from apps.notifications.models import (OwnerInvitation, PublicAuthorization,
                                       Notification)
from apps.notifications.emails import (send_owner_invitation,
                                       send_public_authorization,
                                       send_owner_closed_participation,
                                       send_finish_participations)
from apps.participations.models import InvitedGroup
from wikilegis import celery_app
from celery.utils.log import get_task_logger
from datetime import date, timedelta
from utils.format_text import format_proposal_title

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


def closed_participation_notify(public_group, proposal_title):
    document = public_group.document
    notification = Notification()
    notification.user = document.owner
    message = 'A sua consulta pública sobre o proposição legislativa "{}"  \
               encontra-se encerrada'
    notification.message = message.format(proposal_title)
    notification.save()


@celery_app.task
def notify_closed_participation():
    yesterday = date.today() - timedelta(days=1)

    invited_groups = InvitedGroup.objects.filter(
        closing_date=yesterday,
        public_participation=True
    )

    for invited_group in invited_groups:
        proposal_title = format_proposal_title(invited_group.document)
        closed_participation_notify(invited_group, proposal_title)
        send_owner_closed_participation(invited_group, proposal_title)
        invited_group.group_status = 'waiting_feedback'
        invited_group.save()


@celery_app.task(name="send_feedback_email_task")
def task_send_finish_participations(id_group, proposal_title, slug_document,
                                    user_email):
    send_finish_participations(id_group, proposal_title, slug_document,
                               user_email)
