from django.urls import path
from apps.notifications import views

urlpatterns = [
    path('authorization/<str:user_type>/<uuid:hash>/',
         views.authorization,
         name="authorization"),
]
