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
    path('public-participation/unauthorization/<uuid:hash>/',
         views.PublicUnauthorizationView.as_view(),
         name="unpublic-authorization"),
    path('read/',
         views.update_notifications,
         name="read_notifications"),
    path('teste/',
         views.TesteTemplate.as_view(),
         name="teste"),
    path('diff/',
         views.DiffTemplate.as_view(),
         name="diff")
]
