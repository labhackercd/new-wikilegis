from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.routers import SimpleRouter
from django.contrib.sites.models import Site
from apps.api import api


router = SimpleRouter()
router.register(r'api/v1/users', api.UserViewSet)
router.register(r'api/v1/themes', api.ThemeViewSet)
router.register(r'api/v1/document-types', api.DocumentTypeViewSet)
router.register(r'api/v1/documents', api.DocumentViewSet)
router.register(r'api/v1/excerpts', api.ExcerptViewSet)
router.register(r'api/v1/sugestions', api.SuggestionViewSet)
router.register(r'api/v1/opnion-votes', api.OpinionVoteViewSet)
router.register(r'api/v1/groups', api.InvitedGroupViewSet)
router.register(r'api/v1/thematic-groups', api.ThematicGroupViewSet)


@api_view(['GET'])
def api_root(request, format=None):
    current_site = Site.objects.get_current()
    current_site.domain
    request.META['HTTP_HOST'] = current_site.domain

    return Response({
        'users': reverse('user-list',
                         request=request, format=format),
        'document-types': reverse('documenttype-list',
                                  request=request, format=format),
        'documents': reverse('document-list',
                             request=request, format=format),
        'excerpts': reverse('excerpt-list',
                            request=request, format=format),
        'sugestions': reverse('suggestion-list',
                              request=request, format=format),
        'opnion-votes': reverse('opinionvote-list',
                                request=request, format=format),
        'groups': reverse('invitedgroup-list',
                          request=request, format=format),
        'thematic-groups': reverse('thematicgroup-list',
                                   request=request, format=format),
    })
