from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NotificationsConfig(AppConfig):
    name = 'apps.notifications'
    verbose_name = _('Notifications')

    def ready(self):
        from apps.notifications import tasks # noqa