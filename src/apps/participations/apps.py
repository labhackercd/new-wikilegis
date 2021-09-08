from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ParticipationsConfig(AppConfig):
    name = 'apps.participations'
    verbose_name = _('Participations')

    def ready(self):
        from django.db.models.signals import post_save
        from apps.participations import models, tasks
        post_save.connect(tasks.save_invited_email, sender=models.InvitedGroup)
