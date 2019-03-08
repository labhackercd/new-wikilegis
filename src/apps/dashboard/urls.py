from django.urls import path
from apps.dashboard import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.OwnerDocumentsView.as_view(), name="owner_documents"),
    path('document/<int:pk>', views.EditDocumentView.as_view(),
         name='edit_document'),
    path('groups/', TemplateView.as_view(
         template_name="pages/groups.html", extra_context={'is_owner': True}),
         name='groups')
]
