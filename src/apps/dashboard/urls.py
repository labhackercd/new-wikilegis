from django.urls import path
from apps.projects.views import DocumentUpdateView
from apps.dashboard.views import DocumentEditorClusterView, OwnerDocumentsView
from django.views.generic import TemplateView


urlpatterns = [
    path('', OwnerDocumentsView.as_view(), name="owner_documents"),
    path('<str:template>/document/<int:pk>',
         DocumentEditorClusterView.as_view(),
         name='document_editor_cluster'),
    path('edit/<int:pk>-<slug:documment_slug>/',
         DocumentUpdateView.as_view(), name="edit_document"),
    path('page', TemplateView.as_view(template_name='pages/closing-date.html'),
         name='testpage'),
    # path('groups/', views.OwnerGroupsView.as_view(), name='groups')
]
