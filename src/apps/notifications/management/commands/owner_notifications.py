from django.core.management.base import BaseCommand
from apps.notifications.models import Notification
from apps.participations.models import InvitedGroup
from datetime import datetime


class Command(BaseCommand):
    help = 'Send notifications to document owners'

    def handle(self, *args, **options):
        today = datetime.now().date()
        for group in InvitedGroup.objects.all():
            message = ''
            delta = group.closing_date - today
            if group.public_participation:
                if group.closing_date == today:
                    message = 'A consulta pública do documento %s encerra \
                        hoje, para prorrogar o prazo, altere a data de \
                        encerramento.' % group.document.title
                elif delta.days == -1:
                    message = 'A consulta pública do documento %s \
                        encerrou.' % group.document.title
                elif delta.days == 3:
                    message = 'A consulta pública do documento %s encerra \
                        em 3 dias, para prorrogar o prazo, altere a data de \
                        encerramento.' % group.document.title
            else:
                if group.closing_date == today:
                    message = 'A participação do grupo %s encerra \
                        hoje, para prorrogar o prazo, altere a data de \
                        encerramento.' % group.thematic_group.name
                elif delta.days == -1:
                    message = 'A participação do grupo %s \
                        encerrou.' % group.thematic_group.name
                elif delta.days == 3:
                    message = 'A participação do grupo %s encerra \
                        em 3 dias, para prorrogar o prazo, altere a data de \
                        encerramento.' % group.thematic_group.name
            if message:
                notification = Notification()
                notification.message = message
                notification.user = group.document.owner
                notification.save()
