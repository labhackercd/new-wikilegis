from django.urls import path
from apps.projects import views
from apps.participations.views import (InvitedGroupDetailView,
                                       InvitedGroupAnalyzeView)

urlpatterns = [
    path('<int:id>-<slug:documment_slug>/estatisticas/',
         InvitedGroupAnalyzeView.as_view(),
         name="group-analysis"),
    path('<int:id>-<slug:documment_slug>/',
         InvitedGroupDetailView.as_view(),
         name="project"),
    path('invitation/<int:pk>/<str:accept>/',
         views.InvitationRedirectView.as_view(),
         name="invitation"),
    path('new/', views.DocumentCreateRedirectView.as_view(),
         name="new_document"),
    path('<int:pk>/text/', views.DocumentTextView.as_view(),
         name="document_text"),
    path('diff/<uuid:hash>/',
         views.DocumentDiffTemplateView.as_view(),
         name="diff_version"),
]
