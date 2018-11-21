from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'apps.notifications'

    def ready(self):
        from apps.notifications import tasks # noqa