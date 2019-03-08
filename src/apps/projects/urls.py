from django.urls import path
from django.views.generic import TemplateView
from apps.projects import views
from apps.participations.views import InvitedGroupDetailView

urlpatterns = [
    path('<int:id>-<slug:documment_slug>/',
         InvitedGroupDetailView.as_view(),
         name="project"),
    path('invitation/<int:pk>/<str:accept>/',
         views.InvitationRedirectView.as_view(),
         name="invitation"),
    path('new/', views.DocumentCreateView.as_view(), name="new_document"),
    path('edit/<int:pk>-<slug:documment_slug>/',
         views.DocumentUpdateView.as_view(), name="edit_document"),
    path('document/<int:pk>', views.EditDocumentView.as_view(),
         name='edit_document'),
    path('groups/', TemplateView.as_view(
         template_name="pages/groups.html", extra_context={'is_owner': True}),
         name='groups')
]
