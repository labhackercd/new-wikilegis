from django.urls import path
from apps.participations import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('suggestion/new/<int:group_pk>',
         login_required(views.send_suggestion),
         name='new_suggestion'),
    path('suggestion/undo/<int:suggestion_pk>',
         login_required(views.undo_suggestion),
         name='undo_suggestion'),
    path('suggestion/new-opinion/', login_required(views.new_opinion),
         name='new_opinion'),
    path('invited-group/new/<int:pk>', views.InvitedGroupCreate.as_view(),
         name='new_group'),
]
