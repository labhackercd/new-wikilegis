from django.contrib.auth.models import User
from rest_framework import filters, viewsets
from django_filters import FilterSet
from django_filters import rest_framework as django_filters
from apps.api import serializers
from apps.projects.models import Theme, DocumentType, Document


# Accounts app
class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = {
            'last_login': ['lt', 'gt', 'lte', 'gte', 'year__gt', 'year__lt'],
            'date_joined': ['lt', 'gt', 'lte', 'gte', 'year__gt', 'year__lt'],
            'profile__birthdate': ['lt', 'gt', 'lte', 'gte', 'year__gt',
                                   'year__lt'],
            'profile__uf': ['exact'],
            'profile__gender': ['exact'],
            'profile__country': ['exact'],
        }


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = serializers.UserSerializer
    filter_class = UserFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
    )
    filter_fields = ('id', 'profile__uf')
    search_fields = ('username', 'first_name', 'last_name')
    ordering_fields = '__all__'


# Projects app
class ThemeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = serializers.ThemeSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_fields = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    ordering_fields = '__all__'


class DocumentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = serializers.DocumentTypeSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_fields = ('id', 'title', 'initials')
    search_fields = ('title', 'initials')
    ordering_fields = '__all__'


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Document.objects.all()
    serializer_class = serializers.DocumentSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_fields = ('id', 'themes', 'owner', 'document_type')
    search_fields = ('title', 'slug', 'description', 'number', 'year',
                     'document_type__title', 'document_type__initials')
    ordering_fields = '__all__'
