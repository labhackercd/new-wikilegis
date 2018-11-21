from django.core.exceptions import PermissionDenied
from apps.notifications.models import ParcipantInvitation
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.contrib.auth.models import User


@login_required(login_url='/')
def authorization(request, hash):
    accepted = request.GET.get('accepted', None)
    invited_email = ParcipantInvitation.objects.get(hash_id=hash)
    if request.user.email == invited_email.email:
        if accepted:
            invited_email.accepted = True
            invited_email.save()
            user = User.objects.get(email=invited_email.email)
            for theme in invited_email.group.document.themes.all():
                user.profile.themes.add(theme)
            return HttpResponseRedirect('/')
        else:
            template = loader.get_template('pages/authorization.html')
            context = {
                'hash': hash,
            }
            return HttpResponse(template.render(context, request))
    else:
        raise PermissionDenied
