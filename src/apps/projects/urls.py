from django.urls import path
from apps.projects import views

urlpatterns = [
    path('<int:id>-<slug:slug>/',
         views.DocumentDetailView.as_view(),
         name="project"),
    path('invitation/<int:pk>/<str:accept>/',
         views.InvitationRedirectView.as_view(),
         name="invitation"),
    path('new/', views.DocumentCreateView.as_view(), name="new_document")
]
