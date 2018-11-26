from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from apps.api.urls import router
from apps.projects import views


urlpatterns = [
    path('', views.DocumentListView.as_view(), name='home'),
    path('document/', TemplateView.as_view(template_name='pages/document.html'),
         name='document'),
    path('admin/', admin.site.urls),
    path('notifications/', include('apps.notifications.urls')),
    path('api/v1/', include(router.urls)),
]

admin.site.site_header = 'wikilegis'
