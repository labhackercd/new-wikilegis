from django.urls import path
from apps.notifications import views

urlpatterns = [
    path('information-congressman/<uuid:hash>/',
         views.InformationCongressmanView.as_view(),
         name="information_authorization"),
    path('authorization/<uuid:hash>/',
         views.authorization,
         name="authorization"),
    path('public-participation/authorization/<uuid:hash>/',
         views.PublicAuthorizationView.as_view(),
         name="public-authorization"),
    path('read/',
         views.update_notifications,
         name="read_notifications"),
]
