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
    path('feedback/authorization/<uuid:hash>/',
         views.FeedbackAuthorizationView.as_view(),
         name="feedback_authorization"),
    path('feedback/unauthorization/<uuid:hash>/',
         views.FeedbackUnauthorizationView.as_view(),
         name="feedback_unauthorization"),
    path('feedback-information/<uuid:hash>/',
         views.FeedbackInformationView.as_view(),
         name="feedback_information"),
    path('read/',
         views.update_notifications,
         name="read_notifications"),
]
