from django.views.generic import DetailView, RedirectView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from .models import Document
from .forms import DocumentForm
from apps.notifications.models import ParcipantInvitation
from django.http import Http404, JsonResponse
from django.contrib.sites.models import Site


class DocumentDetailView(DetailView):
    model = Document
    template_name = 'pages/document.html'


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


class DocumentCreateView(CreateView):
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


def list_propositions(request):
    documents = Document.objects.filter(
        invited_groups__public_participation=True,
        document_type__isnull=False).distinct()
    result = []
    for document in documents:
        obj = {
            'numProposicao': document.number,
            'anoProposicao': document.year,
            'siglaTipoProposicao': document.document_type.initials,
            'uri': '%s%s' % (Site.objects.get_current().domain,
                             document.get_absolute_url())
        }
        result.append(obj)

    return JsonResponse(result, safe=False)
