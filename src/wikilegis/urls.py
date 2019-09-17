from django.contrib import admin
from django.urls import path, include
from apps.api.urls import router
from apps.participations import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.InvitedGroupListView.as_view(), name='home'),
    path('dashboard/', include('apps.dashboard.urls')),
    path('admin/', admin.site.urls),
    path('notifications/', include('apps.notifications.urls')),
    path('p/', include('apps.projects.urls')),
    path('api/v1/', include(router.urls)),
    path('participation/', include('apps.participations.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('listarProposicoes/', views.list_propositions),
    path('listarProposicoes/<int:cd_id>', views.proposition_detail),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'wikilegis'
