from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.db.models.aggregates import Count
from utils.decorators import require_ajax
from datetime import date
from random import randint
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from apps.projects.models import Excerpt, Theme, Document
from apps.participations.models import InvitedGroup, Suggestion, OpinionVote
from apps.accounts.models import ThematicGroup
from apps.notifications.models import ParcipantInvitation
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.forms import ValidationError
from django.db.models import Q

User = get_user_model()


class InvitedGroupCreate(CreateView):
    model = InvitedGroup
    template_name = 'pages/invite-participants.html'
    fields = ['closing_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['themes'] = Theme.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.document = Document.objects.get(id=self.kwargs.get('pk'))
        self.object.public_participation = False
        thematic_group = ThematicGroup(owner=self.request.user)
        thematic_group.name = self.request.POST.get('group_name', None)
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
        return reverse_lazy(
            'new_group', kwargs={'pk': self.object.document.id})


class InvitedGroupListView(ListView):
    model = InvitedGroup
    template_name = 'pages/home.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = object_list if object_list is not None else self.object_list
        context['public_groups'] = queryset.filter(public_participation=True)
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

    def get_object(self, queryset=None):
        obj = get_object_or_404(
            InvitedGroup, pk=self.kwargs.get('id'),
            document__slug=self.kwargs.get('documment_slug'))
        if obj.public_participation:
            return obj
        elif self.request.user in obj.thematic_group.participants.all():
            return obj
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

    if invited_group.closing_date > date.today():
        Suggestion.objects.create(
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
            {'excerpt': excerpt, 'request': request}
        )
        return JsonResponse({
            'id': excerpt.id,
            'html': html,
        })
    else:
        return JsonResponse(
            {'error': _('Project closed for participation')},
            status=400
        )


@require_ajax
def get_random_suggestion(request):
    excerpt_id = request.POST.get('excerptId')
    document_id = request.POST.get('documentId')
    opined_suggestions = OpinionVote.objects.filter(
        owner=request.user,
        suggestion__excerpt__document__id=document_id
    ).values_list('suggestion__id', flat=True)

    if excerpt_id:
        suggestions = Suggestion.objects.filter(
            excerpt__id=excerpt_id
        )
    else:
        suggestions = Suggestion.objects.filter(
            excerpt__document__id=document_id
        )

    suggestions = suggestions.exclude(
        author=request.user
    ).exclude(
        id__in=opined_suggestions
    )

    if suggestions.count() > 0:
        count = suggestions.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        print(random_index)

        suggestion = suggestions[random_index]

        span = '<span class="text-highlight">'
        close_span = '</span>'
        content = suggestion.excerpt.content
        content = '{prev}{open_span}{content}{close_span}{after}'.format(
            prev=content[:suggestion.start_index],
            open_span=span,
            content=content[suggestion.start_index:suggestion.end_index],
            close_span=close_span,
            after=content[suggestion.end_index:]
        )

        data = {
            'user': {
                'id': suggestion.author.id,
                'avatar': suggestion.author.profile.avatar_url,
                'fullName': suggestion.author.get_full_name(),
            },
            'excerpt': {
                'id': suggestion.excerpt.id,
                'html': content,
            },
            'suggestion': {
                'id': suggestion.id,
                'text': suggestion.content
            }
        }

        return JsonResponse(data)
    else:
        return JsonResponse({'error': _('No suggestion found')}, status=404)


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
