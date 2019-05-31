from django.contrib.sites.models import Site
from django.conf import settings
import re


def settings_variables(request):
    site_url = Site.objects.get_current().domain
    prefix_url = settings.FORCE_SCRIPT_NAME
    return {'site_url': site_url, 'prefix_url': prefix_url}


def current_url(request):
    if settings.FORCE_SCRIPT_NAME:
        path = re.sub(
            r'^{}'.format(settings.FORCE_SCRIPT_NAME),
            '',
            request.path
        )
    else:
        path = request.path
    return {'current_path': path}
