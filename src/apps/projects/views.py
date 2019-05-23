from django.views.generic import RedirectView, UpdateView, View
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from .models import Document, DocumentVersion
from .forms import DocumentForm
from apps.notifications.models import ParcipantInvitation
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from utils.decorators import owner_required
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from apps.notifications.models import Notification
from django.contrib.auth.models import User


class InvitationRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        invitation = get_object_or_404(ParcipantInvitation, pk=kwargs['pk'])
        invitation.answered = True

        if kwargs['accept'] == 'accepted':
            invitation.accepted = True
            notification = Notification()
            notification.user = invitation.group.document.owner
            participant = User.objects.get(email=invitation.email)
            notification.message = '%s aceitou o convite para participar do \
                                    grupo %s' % (
                participant.get_full_name(),
                invitation.group.thematic_group.name)
            notification.save()
        elif kwargs['accept'] == 'declined':
            invitation.accepted = False
            notification = Notification()
            notification.user = invitation.group.document.owner
            participant = User.objects.get(email=invitation.email)
            notification.message = '%s não aceitou o convite para participar \
                                    do grupo %s' % (
                participant.get_full_name(),
                invitation.group.thematic_group.name)
            notification.save()
        else:
            raise Http404

        invitation.save()

        return reverse(
            'project',
            kwargs={'id': invitation.group.id,
                    'documment_slug': invitation.group.document.slug})


@method_decorator(login_required, name='dispatch')
@method_decorator(owner_required, name='dispatch')
class DocumentCreateRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        document = Document()
        document.owner = self.request.user
        document.save()

        return reverse('document_editor_cluster',
                       kwargs={'template': 'editor',
                               'pk': document.id})


@method_decorator(login_required, name='dispatch')
@method_decorator(owner_required, name='dispatch')
class DocumentUpdateView(UpdateView):
    model = Document
    form_class = DocumentForm
    template_name = 'pages/new-document.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'data' in kwargs.keys():
            data = kwargs['data'].copy()
            data['owner'] = self.request.user.id
            kwargs['data'] = data
        return kwargs

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = True
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(owner_required, name='dispatch')
class DocumentTextView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        document = get_object_or_404(Document, pk=kwargs['pk'])
        version = request.GET.get('version', None)

        try:
            rendered = render_to_string(
                'txt/document_text',
                {'excerpts': document.get_excerpts(version=version)}
            )
            version = document.versions.get(number=version)
            if version.name:
                version_name = version.name
            else:
                version_name = version.created.strftime('%Hh%M - %d de %b, %Y')

            return JsonResponse({'html': rendered,
                                 'versionName': version_name})
        except DocumentVersion.DoesNotExist:
            rendered = render_to_string(
                'txt/document_text',
                {'excerpts': document.get_excerpts()}
            )
            version = document.versions.first()
            if version.name:
                version_name = version.name
            else:
                version_name = version.created.strftime('%Hh%M - %d de %b, %Y')

            return JsonResponse({
                'message': _('Version not found! '
                             'We loaded the last version for you :)'),
                'versionName': version_name,
                'html': rendered
            }, status=404)
