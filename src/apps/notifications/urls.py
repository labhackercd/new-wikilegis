from django.urls import path
from apps.notifications import views

urlpatterns = [
    path('authorization/<uuid:hash>/',
         views.authorization,
         name="authorization"),
]
