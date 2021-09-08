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
    path('invited-group/edit/<int:pk>', views.InvitedGroupUpdateView.as_view(),
         name='edit_group'),
    path('document/<int:excerpt_pk>/opinions', views.get_opinions,
         name='excerpt_opinions'),
    path('invited-group/public/new/<int:document_pk>',
         views.create_public_participation,
         name='new_public_participation'),
    path('invited-group/public/edit/<int:group_id>',
         views.update_closing_date,
         name='update_public_participation'),
    path('invited-group/final-version/<int:group_id>',
         views.set_final_version,
         name='set_final_version'),
    path('invited-group/<int:group_pk>/report/download-csv/',
         views.download_csv,
         name='download-csv'),
]
