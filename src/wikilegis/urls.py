from django.contrib import admin
from django.urls import path, include
from apps.api.urls import router
from apps.participations import views
from django.conf import settings
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from apps.projects.views import list_propositions


urlpatterns = [
    path('', views.InvitedGroupListView.as_view(), name='home'),
    path('document/',
         TemplateView.as_view(template_name='pages/document.html'),
         name='document'),
    path('admin/', admin.site.urls),
    path('notifications/', include('apps.notifications.urls')),
    path('p/', include('apps.projects.urls')),
    path('api/v1/', include(router.urls)),
    path('participation/', include('apps.participations.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('listarProposicoes/', list_propositions),
    path('dashboard/',
         TemplateView.as_view(template_name='pages/dashboard.html'),
         name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'wikilegis'
