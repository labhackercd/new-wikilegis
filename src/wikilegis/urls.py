from django.contrib import admin
from django.urls import path, include, re_path
from apps.api.urls import router, api_root
from apps.reports import urls as reports_urls
from apps.participations import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.sites.models import Site


current_site = Site.objects.get_current()

schema_view = get_schema_view(
    openapi.Info(
        title="Wikilegis API",
        default_version='v1',
        description="Analise as propostas legislativas, contribua dando \
                     sua opinião em trechos do texto e avalie as opiniões \
                     de outros cidadãos.",
        contact=openapi.Contact(email="labhacker@camara.leg.br"),
        license=openapi.License(name="GNU General Public License v3.0"),
    ),
    url='https://' + current_site.domain,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', views.InvitedGroupListView.as_view(), name='home'),
    path('dashboard/', include('apps.dashboard.urls')),
    path('admin/', admin.site.urls),
    path('notifications/', include('apps.notifications.urls')),
    path('p/', include('apps.projects.urls')),
    path('participation/', include('apps.participations.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('listarProposicoes/', views.list_propositions),
    path('listarProposicoes/<int:cd_id>', views.proposition_detail),
]

urlpatterns += router.urls
urlpatterns += [
    path('api/v1/', api_root),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('reports/', include(reports_urls)),
]

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'wikilegis'
