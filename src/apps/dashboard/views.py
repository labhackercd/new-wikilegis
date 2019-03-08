from django.views.generic import ListView, DetailView
from django.http import Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from utils.decorators import owner_required
from apps.projects.models import Document


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
class EditDocumentView(DetailView):
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
        group_id = self.request.GET.get('group_id', None)
        if group_id:
            context['group'] = self.object.invited_groups.get(id=group_id)
        else:
            context['group'] = self.object.invited_groups.first()
        return context
