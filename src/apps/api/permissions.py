from rest_framework import permissions
from django.conf import settings


class ApiKeyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        api_key = request.GET.get('api_key', None)
        if request.method in permissions.SAFE_METHODS:
            return True
        return api_key == settings.SECRET_KEY
