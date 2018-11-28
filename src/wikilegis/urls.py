from django.contrib import admin
from django.urls import path, include
from apps.api.urls import router
from apps.projects import views


urlpatterns = [
    path('', views.DocumentListView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('notifications/', include('apps.notifications.urls')),
    path('p/', include('apps.projects.urls')),
    path('api/v1/', include(router.urls)),
]

admin.site.site_header = 'wikilegis'
