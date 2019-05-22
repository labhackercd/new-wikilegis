from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ProjectsConfig(AppConfig):
    name = 'apps.projects'
    verbose_name = _('Projects')

    def ready(self):
        from django.db.models.signals import post_save
        from apps.projects import models, tasks
        post_save.connect(tasks.create_first_version,
                          sender=models.Document)
