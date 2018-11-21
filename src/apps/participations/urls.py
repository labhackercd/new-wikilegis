from django.urls import path
from apps.participations import views

urlpatterns = [
    path('authorization/<uuid:hash>/',
         views.authorization,
         name="authorization"),
]
