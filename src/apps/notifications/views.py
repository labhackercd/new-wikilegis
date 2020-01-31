from django.core.exceptions import PermissionDenied
from apps.notifications.models import (ParcipantInvitation,
                                       PublicAuthorization, Notification,
                                       FeedbackAuthorization)
from apps.projects.models import Document, DocumentVideo
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages import success
from django.views.generic import RedirectView
from django.shortcuts import get_object_or_404, reverse
from utils.decorators import require_ajax
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse
from datetime import datetime, date
from django.views.generic import TemplateView
from django.http import Http404
from utils.format_text import format_proposal_title
from apps.notifications.emails import (
    send_feedback_authorization_owner_document,
    send_feedback_authorization_management)


@login_required(login_url='/')
def authorization(request, hash):
    participant_invitation = ParcipantInvitation.objects.get(hash_id=hash)
    if request.user.email == participant_invitation.email:
        participant_invitation.accepted = True
        participant_invitation.save()
        user = User.objects.get(email=participant_invitation.email)
        for theme in participant_invitation.group.document.themes.all():
            user.profile.themes.add(theme)
        return reverse('home')
    else:
        raise PermissionDenied


class PublicAuthorizationView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        authorization = get_object_or_404(PublicAuthorization,
                                          hash_id=kwargs['hash'])
        public_group = authorization.group
        public_group.group_status = 'in_progress'
        notification = Notification()
        notification.user = public_group.document.owner
        if authorization.closing_date:
            public_group.closing_date = authorization.closing_date
            document = Document.objects.get(id=authorization.group.document.id)
            document.responsible = authorization.congressman
            document.save()
            notification.message = '%s aceitou seu pedido para alteração da \
                data de \
                encerramento' % (authorization.congressman.name.title())
        else:
            notification.message = '%s aceitou seu pedido para tornar o \
                documento público' % (authorization.congressman.name.title())
            public_group.openning_date = datetime.now()
        notification.save()
        public_group.save()

        return reverse('project',
                       kwargs={'id': public_group.id,
                               'documment_slug': public_group.document.slug})


class PublicUnauthorizationView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        authorization = get_object_or_404(PublicAuthorization,
                                          hash_id=kwargs['hash'])
        public_group = authorization.group
        document = public_group.document
        updated = self.request.GET.get('updated', False)

        if public_group.group_status != 'in_progress':
            if updated:
                message = '{} não aceitou seu pedido de alteração da data \
                     final da consluta pública da proposição {}.'
            else:
                public_group.delete()
                message = '{} não aceitou seu pedido para participação \
                pública da proposição {}.'

            notification = Notification()
            notification.user = document.owner

            proposal_title = format_proposal_title(document)

            notification.message = message.format(
                authorization.congressman.name.title(), proposal_title)

            notification.save()

            return reverse('home')
        else:
            raise Http404


class InformationCongressmanView(TemplateView):
    template_name = 'pages/public_participation_disclaimer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_url = Site.objects.get_current().domain

        authorization = get_object_or_404(PublicAuthorization,
                                          hash_id=kwargs['hash'])
        updated = self.request.GET.get('updated', False)

        context['hash_id'] = authorization.hash_id
        context['site_url'] = site_url
        context['closing_date'] = authorization.closing_date
        context['document'] = authorization.group.document
        context['updated'] = updated

        if authorization.group.group_status == 'in_progress':
            raise Http404

        return context


class FeedbackAuthorizationView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        feedback_authorization = get_object_or_404(FeedbackAuthorization,
                                                   hash_id=kwargs['hash'])
        document = feedback_authorization.group.document

        public_group = feedback_authorization.group
        public_group.final_version = feedback_authorization.version
        public_group.group_status = 'analyzing'
        public_group.save()

        video = DocumentVideo(document=document,
                              video_id=feedback_authorization.video_id)
        video.save()

        notification = Notification()
        notification.user = document.owner
        proposal_title = format_proposal_title(document)

        message = '{} aceitou seu pedido para versão final da \
                proposição {}.'
        notification.message = message.format(
            document.responsible.name.title(), proposal_title)
        notification.save()

        send_feedback_authorization_owner_document(feedback_authorization)
        send_feedback_authorization_management(feedback_authorization)
        success(self.request, _('''The system management will audit the video
                                and document information. Wait please!'''))

        return reverse('home')


class FeedbackUnauthorizationView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        authorization = get_object_or_404(FeedbackAuthorization,
                                          hash_id=kwargs['hash'])
        document = authorization.group.document
        notification = Notification()
        notification.user = document.owner

        proposal_title = format_proposal_title(document)

        message = '{} não aceitou seu pedido para versão final da \
                proposição {}.'
        notification.message = message.format(
            document.responsible.name.title(), proposal_title)

        notification.save()

        return reverse('project',
                       kwargs={'id': authorization.group.id,
                               'documment_slug': document.slug})


class FeedbackInformationView(TemplateView):
    template_name = 'pages/feedback_disclaimer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_url = Site.objects.get_current().domain
        today = date.today()

        authorization = get_object_or_404(FeedbackAuthorization,
                                          hash_id=kwargs['hash'])

        context['hash_id'] = kwargs['hash']
        context['site_url'] = site_url
        context['document'] = authorization.group.document
        context['closing_date'] = authorization.group.closing_date

        if authorization.group.closing_date > today:
            raise Http404

        return context


@require_ajax
def update_notifications(request):
    user = request.user
    user.notifications.update(was_read=True)
    return JsonResponse({'message': _('Notifications read!')})
