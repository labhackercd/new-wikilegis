from django.apps import AppConfig


class ParticipationsConfig(AppConfig):
    name = 'apps.participations'

    def ready(self):
        from django.db.models.signals import post_save
        from apps.participations import models, tasks
        post_save.connect(tasks.save_invited_email, sender=models.InvitedGroup)
