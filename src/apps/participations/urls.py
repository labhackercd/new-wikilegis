from django.urls import path
from apps.participations import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('suggestion/new/', login_required(views.send_suggestion),
         name='new_suggestion'),
]
