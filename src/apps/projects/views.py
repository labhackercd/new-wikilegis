from django.views.generic import RedirectView, UpdateView
from django.shortcuts import get_object_or_404
from .models import Document
from .forms import DocumentForm
from apps.notifications.models import ParcipantInvitation
from django.http import Http404
from django.utils.decorators import method_decorator
from utils.decorators import owner_required
from django.contrib.auth.decorators import login_required
from django.urls import reverse


class InvitationRedirectView(RedirectView):
    url = '/'

    def get_redirect_url(self, *args, **kwargs):
        invitation = get_object_or_404(ParcipantInvitation, pk=kwargs['pk'])
        invitation.answered = True

        if kwargs['accept'] == 'accepted':
            invitation.accepted = True
        elif kwargs['accept'] == 'declined':
            invitation.accepted = False
        else:
            raise Http404

        invitation.save()

        return super().get_redirect_url(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(owner_required, name='dispatch')
class DocumentCreateRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        document = Document()
        document.owner = self.request.user
        document.title = "Nome da proposição"
        document.description = "Adicione aqui a ementa da proposição"
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
