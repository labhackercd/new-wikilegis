from django.urls import path
from apps.notifications import views
from django.views.generic import TemplateView


urlpatterns = [
    path('authorization/<uuid:hash>/',
         views.authorization,
         name="authorization"),
    path('public-participation/authorization/<uuid:hash>/',
         views.PublicAuthorizationView.as_view(),
         name="public-authorization"),
    path('public-participation/authorized/',
         TemplateView.as_view(template_name='pages/group-authorized.html'),
         name="group-authorized"),
]
