from django.urls import path
from django.views.generic import TemplateView
from apps.accounts import views

urlpatterns = [
    path('invitation/',
         TemplateView.as_view(template_name="pages/invite-participants.html")),
    path('participants/autocomplete/',
         views.autocompleteUser, name='autocomplete'),
]
