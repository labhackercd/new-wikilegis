from apps.notifications.models import (ParcipantInvitation,
                                       PublicAuthorization, Notification,
                                       FeedbackAuthorization)
from apps.projects.models import Document, DocumentVideo
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
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
    send_feedback_authorization_management,
    send_feedback_unauthorization_owner_document,
    send_management_authorization,
    send_management_unauthorization)
from django.contrib import messages


class ParcipantInvitationView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        participant_invitation = get_object_or_404(ParcipantInvitation,
                                                   hash_id=kwargs['hash'])
        if self.request.user.is_authenticated:
            if self.request.user.email == participant_invitation.email:
                participant_invitation.accepted = True
                participant_invitation.save()
                group = participant_invitation.group
                user = User.objects.get(email=participant_invitation.email)
                for theme in group.document.themes.all():
                    user.profile.themes.add(theme)

                return reverse('project',
                               kwargs={'id': group.id,
                                       'documment_slug': group.document.slug})
            else:
                messages.warning(self.request, _(
                    'You must be logged with same user received email.'))
                return reverse('home')
        else:
            messages.warning(self.request, _(
                'You must be logged to accept email invitation.'))
            return reverse('home')


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
            notification.message = _('%s accepted your request to change the \
            end date') % (authorization.congressman.name.title())
        else:
            notification.message = _('%s accepted your request to make the \
                document public') % (authorization.congressman.name.title())
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
                message = _('{} did not accept your request to change end date \
                    of the public consultation of the proposition {}.')
            else:
                public_group.delete()
                message = _('{} did not accept your request for public \
                participation of the proposition {}.')

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

        if feedback_authorization.group.group_status == 'waiting_feedback':
            document = feedback_authorization.group.document

            public_group = feedback_authorization.group
            public_group.group_status = 'analyzing'
            public_group.save()

            notification = Notification()
            notification.user = document.owner
            proposal_title = format_proposal_title(document)

            message = _('{} accepted your request for final version of \
            proposal {}. The management will audit it.')
            notification.message = message.format(
                document.responsible.name.title(), proposal_title)
            notification.save()

            send_feedback_authorization_management(feedback_authorization)
            send_feedback_authorization_owner_document(feedback_authorization)
            messages.success(self.request, _(
                '''The system management will audit the video
                and document information. Wait please!'''))

            return reverse('home')

        else:
            raise Http404


class FeedbackUnauthorizationView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        feedback_authorization = get_object_or_404(FeedbackAuthorization,
                                                   hash_id=kwargs['hash'])
        if feedback_authorization.group.group_status == 'waiting_feedback':
            document = feedback_authorization.group.document
            notification = Notification()
            notification.user = document.owner

            proposal_title = format_proposal_title(document)

            feedback_authorization.delete()

            message = _('{} did not accept your request for final version of \
                        proposal {}.')
            notification.message = message.format(
                document.responsible.name.title(), proposal_title)

            notification.save()
            send_feedback_unauthorization_owner_document(
                feedback_authorization)
            messages.info(self.request, _('The feedback was rejected!'))

            return reverse('home')

        else:
            raise Http404


class FeedbackAuthorizationManagementView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        feedback_authorization = get_object_or_404(FeedbackAuthorization,
                                                   hash_id=kwargs['hash'])

        if feedback_authorization.group.group_status == 'analyzing':
            document = feedback_authorization.group.document

            public_group = feedback_authorization.group
            public_group.final_version = feedback_authorization.version
            public_group.group_status = 'finished'
            public_group.save()

            video = DocumentVideo(document=document,
                                  video_id=feedback_authorization.video_id,
                                  title=_('Vídeo feedback'))
            video.save()

            notification = Notification()
            notification.user = document.owner
            proposal_title = format_proposal_title(document)

            message = _('The management accepted feedback of proposal {}.')
            notification.message = message.format(
                document.responsible.name.title(), proposal_title)
            notification.save()

            send_management_authorization(feedback_authorization)
            messages.success(self.request, _(
                'The feeback participation was approved!'))

            return reverse('home')

        else:
            raise Http404


class FeedbackUnauthorizationManagementView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        feedback_authorization = get_object_or_404(FeedbackAuthorization,
                                                   hash_id=kwargs['hash'])
        if feedback_authorization.group.group_status == 'analyzing':
            document = feedback_authorization.group.document
            notification = Notification()
            notification.user = document.owner

            proposal_title = format_proposal_title(document)

            feedback_authorization.delete()

            message = _('The management refused the feedback of proposal {}, \
            contat us for more information.')

            notification.message = message.format(proposal_title)

            notification.save()
            send_management_unauthorization(feedback_authorization)
            messages.info(self.request, _('The feedback was rejected!'))

            return reverse('home')

        else:
            raise Http404


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
