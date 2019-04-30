from django.urls import path
from apps.dashboard import views


urlpatterns = [
    path('', views.OwnerDocumentsView.as_view(), name="owner_documents"),
    path('document/<int:pk>', views.EditDocumentView.as_view(),
         name='edit_document'),
    # path('groups/', views.OwnerGroupsView.as_view(), name='groups')
]
