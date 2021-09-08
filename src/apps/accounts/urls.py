from django.urls import path
from apps.accounts import views

urlpatterns = [
    path('participants/autocomplete/',
         views.participants_autocomplete, name='participants_autocomplete'),
    path('participants/email-list/',
         views.email_list_participants, name='email_list_participants'),
]
