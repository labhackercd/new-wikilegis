from rest_framework.routers import DefaultRouter
from apps.api import api


router = DefaultRouter()
router.register(r'users', api.UserViewSet)
router.register(r'documents', api.DocumentViewSet)
router.register(r'document-types', api.DocumentTypeViewSet)
router.register(r'themes', api.ThemeViewSet)
