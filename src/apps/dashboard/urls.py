from django.urls import path
from apps.projects.views import DocumentUpdateView
from apps.dashboard import views


urlpatterns = [
    path('', views.OwnerDocumentsView.as_view(), name="owner_documents"),
    path('<str:template>/document/<int:pk>',
         views.DocumentEditorClusterView.as_view(),
         name='document_editor_cluster'),
    path('editor/document/<int:pk>/save/',
         views.SaveDocumentView.as_view(),
         name='save_document'),
    path('editor/document/<int:pk>/versions/',
         views.ListDocumentVersionsView.as_view(),
         name='list_document_versions'),
    path('edit/<int:pk>-<slug:documment_slug>/',
         DocumentUpdateView.as_view(), name="edit_document"),
]
