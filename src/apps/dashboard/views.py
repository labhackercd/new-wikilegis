from django.views.generic import ListView, DetailView, View
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from utils.decorators import owner_required
from constance import config
from apps.projects.models import Document, DocumentVersion
from apps.projects.parser import parse_html
from datetime import datetime


@method_decorator(login_required, name='dispatch')
@method_decorator(owner_required, name='dispatch')
class OwnerDocumentsView(ListView):
    model = Document
    template_name = 'pages/dashboard.html'

    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = True

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(owner_required, name='dispatch')
class DocumentEditorClusterView(DetailView):
    model = Document
    template_name = 'pages/edit-document.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = True
        context['private_groups'] = self.object.invited_groups.filter(
            public_participation=False)
        context['public_group'] = self.object.invited_groups.filter(
            public_participation=True)[:1]
        context['api_url'] = config.CD_OPEN_DATA_URL
        context['legislature'] = config.CD_CURRENT_LEGISLATURE

        page = self.kwargs['template']
        context['page'] = page
        group_id = self.request.GET.get('group_id', None)
        if page == 'clusters':
            if group_id:
                context['group'] = self.object.invited_groups.get(id=group_id)
            else:
                context['group'] = self.object.invited_groups.first()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(owner_required, name='dispatch')
class SaveDocumentView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        document = get_object_or_404(Document, pk=kwargs['pk'])

        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        html = request.POST.get('html', None)

        last_version = document.versions.first()
        if last_version:
            number = last_version.number + 1
        else:
            number = 1

        version = DocumentVersion.objects.create(
            document=document,
            number=number
        )
        if html:
            parse_html(html, version, document)

        document.title = title
        document.description = description
        document.save()

        return JsonResponse({
            'message': _('Document saved successfully!'),
            'updated': version.created.strftime('%d/%m/%Y às %H:%M')
        })
