from django.contrib.sites.models import Site


def settings_variables(request):
    site_url = Site.objects.get_current().domain
    return {'site_url': site_url}
