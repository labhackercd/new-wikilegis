from django.urls import path
from apps.projects import views

urlpatterns = [
    path('<int:id>-<slug:slug>/',
         views.DocumentDetailView.as_view(),
         name="project"),
]
