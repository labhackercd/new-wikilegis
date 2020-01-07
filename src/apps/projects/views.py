from django.views.generic import RedirectView, UpdateView, View, TemplateView
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from .models import Document, DocumentVersion, Excerpt
from .forms import DocumentForm
from apps.notifications.models import ParcipantInvitation
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from utils.decorators import owner_required
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from apps.notifications.models import Notification, FeedbackAuthorization
from django.contrib.auth.models import User
import diff_match_patch as dmp_module


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

        return reverse('document_editor_analyze',
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
        context['previous_page'] = self.request.GET.get('previous_page', '')
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(owner_required, name='dispatch')
class DocumentTextView(View):
    http_method_names = ['get']

    def get_json_data(self, document, version, text_format='editor'):
        if version.name:
            version_name = version.name
        else:
            version_name = version.created.strftime('%Hh%M - %d de %b, %Y')

        rendered = render_to_string(
            'txt/document_text.txt',
            {'excerpts': document.get_excerpts(version=version.number),
             'format': text_format}
        )

        return {
            'html': rendered.strip(),
            'versionName': version_name,
            'versionNumber': version.number,
            'date': version.created.strftime('%Hh%M - %d de %b, %Y'),
            'autoSave': version.auto_save
        }

    def get(self, request, *args, **kwargs):
        document = get_object_or_404(Document, pk=kwargs['pk'])
        version = request.GET.get('version', None)
        text_format = request.GET.get('format', 'editor')

        try:
            version = document.versions.get(number=version)
            return JsonResponse(self.get_json_data(
                document, version, text_format)
            )
        except ValueError:
            version = document.versions.first()
            return JsonResponse(self.get_json_data(
                document, version, text_format)
            )
        except DocumentVersion.DoesNotExist:
            version = document.versions.first()
            data = self.get_json_data(document, version, text_format)
            data['message'] = _('Version not found! '
                                'We loaded the last version for you :)')
            return JsonResponse(data, status=404)


class DocumentDiffTemplateView(TemplateView):
    template_name = "pages/diff.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hash_id = kwargs['hash']
        feedback_authorization = get_object_or_404(FeedbackAuthorization,
                                                   hash_id=hash_id)

        first_excerpts = self.get_first_text(feedback_authorization)
        final_excerpts = self.get_final_text(feedback_authorization)

        diff_text = self.get_diff(first_excerpts, final_excerpts)

        context['diff_text'] = diff_text
        context['group'] = feedback_authorization.group
        context['is_congressman'] = True

        return context

    def get_diff(self, first_excerpts, final_excerpts):
        dmp = dmp_module.diff_match_patch()

        full_first_text = self.fortmat_text(first_excerpts)
        full_final_text = self.fortmat_text(final_excerpts)

        diff = dmp.diff_main(full_first_text, full_final_text)
        dmp.diff_cleanupSemantic(diff)

        return diff

    def get_first_text(self, feedback_authorization):
        first_version = feedback_authorization.group.version
        first_excerpts = Excerpt.objects.filter(
            version=first_version).order_by('-order')

        return first_excerpts

    def get_final_text(self, feedback_authorization):
        final_version = feedback_authorization.version
        final_excerpts = Excerpt.objects.filter(
            version=final_version).order_by('-order')

        return final_excerpts

    def fortmat_text(self, list_excerpt):
        text = ''
        for excerpt in list_excerpt:
            excerpt_apresentation = (excerpt.excerpt_type.name +
                                     '-' + str(excerpt.number))

            if excerpt.excerpt_type.align_center:
                excerpt_apresentation = excerpt_apresentation + '<br>'

            text = (excerpt.excerpt_type.name + ' - ' + str(excerpt.number) +
                    ' ' + excerpt.content + '<br><br><br>' + text)
        return text
