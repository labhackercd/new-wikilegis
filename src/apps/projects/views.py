from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Document
from datetime import date
from apps.participations.models import InvitedGroup
from apps.notifications.models import ParcipantInvitation


class DocumentListView(ListView):
    model = Document
    template_name = 'pages/home.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = object_list if object_list is not None else self.object_list
        public_doc_ids = InvitedGroup.objects.filter(
            is_open=True).values_list('document', flat=True)
        context['public_docs'] = queryset.filter(id__in=public_doc_ids)
        if self.request.user.is_authenticated:
            user = self.request.user
            accepted_invitations = ParcipantInvitation.objects.filter(
                email=user.email, accepted=True)
            private_doc_ids = [
                invite.group.document.id for invite in accepted_invitations]
            context['private_docs'] = queryset.filter(id__in=private_doc_ids)
            invitations = ParcipantInvitation.objects.filter(
                email=user.email, accepted=False, answered=False)
            doc_invitations_ids = [
                invite.group.document.id
                for invite in invitations
                if invite.group.closing_date >= date.today()]
            context['pending_invites'] = queryset.filter(
                id__in=doc_invitations_ids)
        else:
            context['private_docs'] = queryset.none()
            context['pending_invites'] = queryset.none()

        return context

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = self.model._default_manager.all()
        if q:
            queryset = queryset.filter(
                Q(title__contains=q) | Q(description__contains=q))

        return queryset


class DocumentDetailView(DetailView):
    model = Document
    template_name = 'pages/document.html'
