from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ReportsConfig(AppConfig):
    name = 'apps.reports'
    verbose_name = _('Reports')
