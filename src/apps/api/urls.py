from rest_framework.routers import DefaultRouter
from apps.api import api


router = DefaultRouter()
router.register(r'users', api.UserViewSet)
router.register(r'themes', api.ThemeViewSet)
router.register(r'document-types', api.DocumentTypeViewSet)
router.register(r'documents', api.DocumentViewSet)
router.register(r'excerpts', api.ExcerptViewSet)
router.register(r'sugestions', api.SuggestionViewSet)
router.register(r'opnion-votes', api.OpinionVoteViewSet)
router.register(r'groups', api.InvitedGroupViewSet)
router.register(r'thematic-groups', api.ThematicGroupViewSet)
