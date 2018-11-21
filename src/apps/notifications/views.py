from django.core.exceptions import PermissionDenied
from apps.notifications.models import ParcipantInvitation, OwnerInvitation
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.contrib.auth.models import User


@login_required(login_url='/')
def authorization(request, user_type, hash):
    accepted = request.GET.get('accepted', None)
    if user_type == 'participant':
        participant_invitation = ParcipantInvitation.objects.get(hash_id=hash)
        if request.user.email == participant_invitation.email:
            if accepted:
                participant_invitation.accepted = True
                participant_invitation.save()
                user = User.objects.get(email=participant_invitation.email)
                for theme in participant_invitation.group.document.themes.all():
                    user.profile.themes.add(theme)
                return HttpResponseRedirect('/')
            else:
                template = loader.get_template(
                    'pages/participant-authorization.html')
                context = {
                    'hash': hash,
                }
                return HttpResponse(template.render(context, request))
        else:
            raise PermissionDenied
    elif user_type == 'owner':
        owner_invitation = OwnerInvitation.objects.get(hash_id=hash)
        if request.user.email == owner_invitation.email:
            if accepted:
                owner_invitation.accepted = True
                owner_invitation.save()
                user = User.objects.get(email=owner_invitation.email)
                user.profile.profile_type = 'owner'
                user.profile.save()
                return HttpResponseRedirect('/')
            else:
                template = loader.get_template('pages/owner-authorization.html')
                context = {
                    'hash': hash,
                }
                return HttpResponse(template.render(context, request))
        else:
            raise PermissionDenied
    else:
        raise Http404
