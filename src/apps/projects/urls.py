from django.urls import path
from apps.projects import views
from apps.participations.views import InvitedGroupDetailView

urlpatterns = [
    path('<int:id>-<slug:documment_slug>/',
         InvitedGroupDetailView.as_view(),
         name="project"),
    path('invitation/<int:pk>/<str:accept>/',
         views.InvitationRedirectView.as_view(),
         name="invitation"),
    path('new/', views.DocumentCreateView.as_view(), name="new_document")
]
