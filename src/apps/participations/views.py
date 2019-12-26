from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from utils.decorators import require_ajax
from datetime import date, datetime
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView
from apps.projects.models import (
    Excerpt, Theme, Document, DocumentResponsible, DocumentInfo, DocumentVideo)
from apps.projects.templatetags.projects_tags import excerpt_numbering
from apps.participations.models import InvitedGroup, Suggestion, OpinionVote
from apps.accounts.models import ThematicGroup
from apps.notifications.models import (
    ParcipantInvitation, PublicAuthorization, FeedbackAuthorization)
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.forms import ValidationError
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib.sites.models import Site
from django.utils.decorators import method_decorator
from utils.decorators import owner_required
from django.contrib.auth.decorators import login_required
from constance import config
from apps.notifications.emails import (
    send_remove_participant, send_feedback_authorization)
from utils.filters import get_id_video
import requests
import csv

User = get_user_model()


@method_decorator(login_required, name='dispatch')
@method_decorator(owner_required, name='dispatch')
class InvitedGroupCreate(SuccessMessageMixin, CreateView):
    model = InvitedGroup
    template_name = 'pages/invite-participants.html'
    fields = ['closing_date', 'version']
    success_message = "Grupo criado com sucesso"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['themes'] = Theme.objects.all()
        context['previous_page'] = self.request.GET.get('previous_page', '')
        document = Document.objects.get(id=self.kwargs.get('pk'))
        context['versions'] = document.versions.filter(
            auto_save=False,
            name__isnull=False
        )

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        today = date.today()
        if self.object.closing_date < today:
            form.add_error('closing_date', ValidationError(
                _('Closing date must be greater than or equal to today!')))
            return super().form_invalid(form)
        self.object.document = Document.objects.get(id=self.kwargs.get('pk'))
        self.object.public_participation = False
        group_name = self.request.POST.get('group_name', None)
        if not group_name:
            form.add_error(None, ValidationError(
                _('Group name is required')))
            return super().form_invalid(form)
        thematic_group = ThematicGroup(owner=self.request.user)
        thematic_group.name = group_name
        thematic_group.save()
        participants_ids = self.request.POST.getlist('participants', [])
        emails = self.request.POST.getlist('emails', None)
        if emails:
            for email in emails:
                email_user = User.objects.create(
                    email=email, username=email, is_active=False)
                participants_ids.append(email_user.id)
        if participants_ids:
            participants = User.objects.filter(id__in=participants_ids)
            thematic_group.participants.set(participants)
        if not len(participants_ids):
            form.add_error(None, ValidationError(
                _('Participants are required')))
            return super().form_invalid(form)
        self.object.thematic_group = thematic_group

        self.object.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('document_editor_analyze',
                            kwargs={'template': 'editor',
                                    'pk': self.object.document.id})


@method_decorator(login_required, name='dispatch')
@method_decorator(owner_required, name='dispatch')
class InvitedGroupUpdateView(SuccessMessageMixin, UpdateView):
    model = InvitedGroup
    template_name = 'pages/invite-participants.html'
    fields = ['closing_date']
    success_message = "Grupo alterado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['themes'] = Theme.objects.all()
        context['previous_page'] = self.request.GET.get('previous_page', '')
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.document.owner != self.request.user:
            raise Http404
        elif obj.public_participation:
            raise Http404
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        today = date.today()
        if self.object.closing_date < today:
            form.add_error('closing_date', ValidationError(
                _('Closing date must be greater than or equal to today!')))
            return super().form_invalid(form)
        group_name = self.request.POST.get('group_name', None)
        if not group_name:
            form.add_error(None, ValidationError(
                _('Group name is required')))
            return super().form_invalid(form)
        thematic_group = self.object.thematic_group
        thematic_group.name = group_name
        thematic_group.save()
        participants_ids = self.request.POST.getlist('participants', [])
        emails = self.request.POST.getlist('emails', None)
        if emails:
            for email in emails:
                email_user = User.objects.create(
                    email=email, username=email, is_active=False)
                participants_ids.append(email_user.id)
        if participants_ids:
            new_participants = User.objects.filter(id__in=participants_ids)
            old_participants = thematic_group.participants.all()
            if set(new_participants) != set(old_participants):
                for old_participant in old_participants:
                    if old_participant not in new_participants:
                        old_invitation = ParcipantInvitation.objects.get(
                            group=self.object, email=old_participant.email)
                        old_invitation.delete()
                        send_remove_participant(self.object.document,
                                                old_participant.email)
            thematic_group.participants.set(new_participants)
        if not len(participants_ids):
            form.add_error(None, ValidationError(
                _('Participants are required')))
            return super().form_invalid(form)
        self.object.thematic_group = thematic_group
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('document_editor_analyze',
                            kwargs={'template': 'editor',
                                    'pk': self.object.document.id})


class InvitedGroupListView(ListView):
    model = InvitedGroup
    template_name = 'pages/home.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = object_list if object_list is not None else self.object_list
        context['open_public_groups'] = queryset.filter(
            public_participation=True,
            group_status='in_progress',
            closing_date__gte=date.today()
        ).order_by('closing_date')
        context['closed_public_groups'] = queryset.filter(
            public_participation=True,
            group_status__in=['in_progress', 'waiting_feedback'],
            closing_date__lt=date.today()
        ).order_by('-closing_date')

        if self.request.user.is_authenticated:
            user = self.request.user
            accepted_invitations = ParcipantInvitation.objects.filter(
                email=user.email, accepted=True)
            private_groups_ids = [
                invite.group.id for invite in accepted_invitations]
            context['private_groups'] = queryset.filter(
                id__in=private_groups_ids)
            invitations = ParcipantInvitation.objects.filter(
                email=user.email, accepted=False, answered=False).exclude(
                group__closing_date__lt=date.today())
            context['pending_invites'] = invitations
        else:
            context['private_groups'] = queryset.none()
            context['pending_invites'] = queryset.none()

        if self.request.user.is_superuser:
            context['pending_groups'] = queryset.filter(
                public_participation=True,
                group_status='analyzing'
            ).order_by('closing_date')
        else:
            context['pending_groups'] = queryset.none()

        return context

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = self.model._default_manager.all()
        if q:
            queryset = queryset.filter(
                Q(document__title__contains=q) | Q(
                    document__description__contains=q))

        return queryset


class InvitedGroupDetailView(DetailView):
    model = InvitedGroup
    template_name = 'pages/document.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        suggestions = self.object.suggestions.all()
        if self.request.user.is_authenticated:
            opined_ids = self.request.user.votes.filter(
                suggestion__invited_group=self.object,
            ).values_list('suggestion__id', flat=True)
            suggestions = suggestions.exclude(
                author=self.request.user
            ).exclude(
                id__in=opined_ids
            )
        context['suggestions'] = suggestions
        return context

    def get_object(self, queryset=None):
        obj = get_object_or_404(
            InvitedGroup, pk=self.kwargs.get('id'),
            document__slug=self.kwargs.get('documment_slug'),
            group_status__in=['in_progress', 'analyzing', 'waiting_feedback'])
        if (obj.public_participation and
                obj.group_status in ['in_progress', 'waiting_feedback']):
            return obj
        elif (self.request.user.is_superuser and
              obj.group_status == 'analyzing'):
            return obj
        elif obj.thematic_group:
            if self.request.user in obj.thematic_group.participants.all():
                return obj
            else:
                raise Http404()
        else:
            raise Http404()


@require_ajax
def send_suggestion(request, group_pk):
    excerpt_id = request.POST.get('excerptId')
    content = request.POST.get('suggestion')
    start_index = int(request.POST.get('startSelection'))
    end_index = int(request.POST.get('endSelection'))
    excerpt = get_object_or_404(Excerpt, pk=excerpt_id)
    invited_group = get_object_or_404(InvitedGroup, pk=group_pk)

    if invited_group.closing_date >= date.today():
        suggestion = Suggestion.objects.create(
            invited_group=invited_group,
            selected_text=excerpt.content[start_index:end_index],
            start_index=start_index,
            end_index=end_index,
            excerpt=excerpt,
            content=content,
            author=request.user,
        )
        html = render_to_string(
            'components/document-excerpt.html',
            {'excerpt': excerpt, 'group': invited_group, 'request': request}
        )
        return JsonResponse({
            'id': excerpt.id,
            'html': html,
            'undoUrl': reverse_lazy(
                'undo_suggestion',
                kwargs={'suggestion_pk': suggestion.id}
            )
        })
    else:
        return JsonResponse(
            {'error': _('Project closed for participation')},
            status=400
        )


@require_ajax
def undo_suggestion(request, suggestion_pk):
    suggestion = get_object_or_404(Suggestion, pk=suggestion_pk)
    timediff = timezone.now() - suggestion.created

    if timediff.total_seconds() < 60:
        suggestion.delete()
        html = render_to_string(
            'components/document-excerpt.html', {
                'excerpt': suggestion.excerpt,
                'group': suggestion.invited_group,
                'request': request
            }
        )

        data = {
            'action': 'undo',
            'suggestion': {
                'selectedText': suggestion.selected_text,
                'content': suggestion.content,
                'excerptId': suggestion.excerpt.id,
                'excerptHtml': html
            }
        }
        return JsonResponse(data)
    else:
        return JsonResponse(
            {'error': _('You cannot undo this suggestion after 1 minute')},
            status=400
        )


@require_ajax
def new_opinion(request):
    suggestion_id = request.POST.get('suggestionId')
    opinion = request.POST.get('opinion')
    suggestion = get_object_or_404(Suggestion, pk=suggestion_id)
    OpinionVote.objects.create(
        suggestion=suggestion,
        owner=request.user,
        opinion_vote=opinion
    )
    return JsonResponse({
        'documentId': suggestion.excerpt.document.id,
        'excerptId': suggestion.excerpt.id
    })


@require_ajax
def get_opinions(request, excerpt_pk):
    excerpt = get_object_or_404(Excerpt, pk=excerpt_pk)
    group_pk = request.POST.get('groupId', None)
    if group_pk:
        group = get_object_or_404(InvitedGroup, pk=group_pk)
    else:
        group = excerpt.document.invited_groups.first()
    opinions = excerpt.suggestions.filter(invited_group=group).annotate(
        num_votes=Count('votes')).order_by('-num_votes')
    html = render_to_string(
        'components/opinions-metrics.html', {
            'opinions': opinions,
        }
    )

    return JsonResponse({'opinionsHtml': html})


@require_ajax
def create_public_participation(request, document_pk):
    today = date.today()
    document = Document.objects.get(id=document_pk)
    congressman_id = request.POST.get('congressman_id', None)
    closing_date = request.POST.get('closing_date', None)
    url_video = request.POST.get('url_video', None)

    video_id = get_id_video(url_video)

    if video_id is None:
        return JsonResponse(
            {'error':
             _('Invalid link YouTube. Please enter a valid link!')},
            status=400
        )

    version = request.POST.get('versionId', None)
    if version:
        version = document.versions.get(id=version)
    else:
        return JsonResponse(
            {'error':
             _('You must create a version from your text before '
               'open to participation')},
            status=409
        )

    try:
        end_date = datetime.strptime(closing_date, "%d/%m/%Y").date()
    except Exception:
        return JsonResponse(
            {'error':
             _('Closing date is required!')},
            status=400
        )

    if congressman_id and closing_date:
        if end_date < today:
            return JsonResponse(
                {'error':
                    _('Closing date must be greater than or equal to today!')},
                status=400
            )
        else:
            document_video, created = DocumentVideo.objects.get_or_create(
                document=document)
            document_video.video_id = video_id
            document_video.save()

            group, created = InvitedGroup.objects.get_or_create(
                document=document, public_participation=True,
                defaults={
                    'closing_date': end_date,
                    'version': version
                })
            if created:
                group.group_status = 'waiting'
                group.save()
                url = config.CD_OPEN_DATA_URL + 'deputados/' + congressman_id
                data = requests.get(url).json()
                congressman = data['dados']['ultimoStatus']
                responsible = DocumentResponsible.objects.get_or_create(
                    cd_id=congressman_id)[0]
                responsible.name = congressman['nome']
                responsible.image_url = congressman['urlFoto']
                responsible.party_initials = congressman['siglaPartido']
                responsible.uf = congressman['siglaUf']
                responsible.email = congressman['gabinete']['email']
                responsible.phone = congressman['gabinete']['telefone']
                responsible.save()
                document.responsible = responsible
                document.save()
                PublicAuthorization.objects.create(
                    congressman=responsible, group=group)

                return JsonResponse(
                    {'message': _('Request sent!')})
            else:
                return JsonResponse(
                    {'error':
                     _('You cannot request a public participation again')},
                    status=409
                )
    else:
        return JsonResponse(
            {'error': _('Congressman is required!')},
            status=400
        )


@require_ajax
def update_closing_date(request, group_id):
    today = date.today()
    group = InvitedGroup.objects.get(id=group_id)
    congressman_id = request.POST.get('congressman_id', None)
    closing_date = request.POST.get('closing_date', None)
    end_date = datetime.strptime(closing_date, "%d/%m/%Y").date()
    if congressman_id and closing_date:
        if end_date < today:
            return JsonResponse(
                {'error':
                    _('Closing date must be greater than or equal to today!')},
                status=400
            )
        else:
            url = config.CD_OPEN_DATA_URL + 'deputados/' + congressman_id
            data = requests.get(url).json()
            congressman = data['dados']['ultimoStatus']
            responsible = DocumentResponsible.objects.get_or_create(
                cd_id=congressman_id)[0]
            responsible.name = congressman['nome']
            responsible.image_url = congressman['urlFoto']
            responsible.party_initials = congressman['siglaPartido']
            responsible.uf = congressman['siglaUf']
            responsible.email = congressman['gabinete']['email']
            responsible.phone = congressman['gabinete']['telefone']
            responsible.save()
            PublicAuthorization.objects.create(
                group=group,
                congressman=responsible,
                closing_date=end_date)

            return JsonResponse(
                {'message': _('Request sent!')})
    else:
        return JsonResponse(
            {'error': _('Congressman and closing date are required!')},
            status=400
        )


# Endpoint to link document with Câmara dos Deputados
def list_propositions(request):
    groups = InvitedGroup.objects.filter(
        public_participation=True,
        group_status='in_progress',
        document__document_type__isnull=False).distinct()
    result = []
    for group in groups:
        if hasattr(group.document, 'infos'):
            obj = {
                'id': group.document.infos.cd_id,
                'numProposicao': group.document.number,
                'anoProposicao': group.document.year,
                'siglaTipoProposicao': group.document.document_type.initials,
                'uri': '%s%s' % (Site.objects.get_current().domain,
                                 group.get_absolute_url())
            }
        else:
            obj = {
                'numProposicao': group.document.number,
                'anoProposicao': group.document.year,
                'siglaTipoProposicao': group.document.document_type.initials,
                'uri': 'https://%s%s' % (Site.objects.get_current().domain,
                                         group.get_absolute_url())
            }
        result.append(obj)

    return JsonResponse(result, safe=False)


# Endpoint to link document with Câmara dos Deputados
def proposition_detail(request, cd_id):
    doc_info = get_object_or_404(DocumentInfo, cd_id=cd_id)
    pub_group = doc_info.document.invited_groups.filter(
        group_status='in_progress').first()
    obj = {
        'id': doc_info.cd_id,
        'numProposicao': doc_info.document.number,
        'anoProposicao': doc_info.document.year,
        'siglaTipoProposicao': doc_info.document.document_type.initials,
        'uri': 'https://%s%s' % (Site.objects.get_current().domain,
                                 pub_group.get_absolute_url())
    }

    return JsonResponse(obj, safe=False)


@require_ajax
def set_final_version(request, group_id):
    group = InvitedGroup.objects.get(id=group_id)
    version_id = request.POST.get('version_id', None)
    video_url = request.POST.get('youtube_url', None)

    video_id = get_id_video(video_url)

    if video_id is None:
        return JsonResponse(
            {'error':
             _('Invalid link YouTube. Please enter a valid link!')},
            status=400
        )

    if version_id and video_id:
        final_version = group.document.versions.get(id=version_id)
        if group.version == final_version:
            return JsonResponse(
                {'error':
                 _('Final version must be diferent the initial version!')},
                status=400
            )
        else:
            authorization = FeedbackAuthorization()
            authorization.version = final_version
            authorization.group = group
            authorization.video_id = video_id
            authorization.save()
            send_feedback_authorization(authorization)
            return JsonResponse({'message': _('Request sent!')})
    else:
        return JsonResponse(
            {'error': _('Version and Video link are required!')},
            status=400
        )


class InvitedGroupAnalyzeView(DetailView):
    model = InvitedGroup
    template_name = 'pages/group-analysis.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(
            InvitedGroup, pk=self.kwargs.get('id'),
            document__slug=self.kwargs.get('documment_slug'),
            group_status__in=['in_progress', 'analyzing', 'waiting_feedback'])
        if (obj.public_participation and
                obj.group_status in ['in_progress', 'waiting_feedback']):
            return obj
        elif (self.request.user.is_superuser and
              obj.group_status == 'analyzing'):
            return obj
        elif obj.thematic_group:
            if self.request.user in obj.thematic_group.participants.all():
                return obj
            else:
                raise Http404()
        else:
            raise Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        group = self.object
        group_opinions = Suggestion.objects.filter(invited_group=group)
        group_author_opinions = group_opinions.values_list(
            'author_id', flat=True)
        group_opinions_ids = group_opinions.values_list('id', flat=True)
        group_author_votes = OpinionVote.objects.filter(
            suggestion_id__in=group_opinions_ids).values_list(
            'owner_id', flat=True)
        participants_ids = set(list(group_author_votes) +
                               list(group_author_opinions))
        context['group'] = group
        context['analysis_page'] = True
        context['participation_count'] = len(participants_ids)

        return context


def download_csv(request, group_pk):
    group = InvitedGroup.objects.get(id=group_pk)
    suggestions = group.suggestions.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % (
        group.document.slug)
    writer = csv.writer(response)
    writer.writerow([_('Excerpt'), _('Selected Text'), _('Suggestion'),
                     _('Approve Votes'), _('Reject Votes'), _('Neutral Votes'),
                     _('Total Votes'), _('Autor')])

    for suggestion in suggestions:
        excerpt_content = "%s %s" % (excerpt_numbering(suggestion.excerpt),
                                     suggestion.excerpt.content)
        writer.writerow([
            excerpt_content,
            suggestion.selected_text,
            suggestion.content,
            suggestion.votes_count('approve'),
            suggestion.votes_count('reject'),
            suggestion.votes_count('neutral'),
            suggestion.votes_count(),
            suggestion.author.get_full_name()
        ])

    return response
