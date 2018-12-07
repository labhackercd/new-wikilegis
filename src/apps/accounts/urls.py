from django.urls import path
from apps.accounts import views

urlpatterns = [
    path('participants/autocomplete/',
         views.autocompleteUser, name='autocomplete'),
]
