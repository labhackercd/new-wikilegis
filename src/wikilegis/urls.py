from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from apps.accounts.api import UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', TemplateView.as_view(template_name='pages/home.html'),
         name='home'),
    path('admin/', admin.site.urls),
    path('notifications/', include('apps.notifications.urls')),
    path('api/v1/', include(router.urls)),
]

admin.site.site_header = 'wikilegis'
