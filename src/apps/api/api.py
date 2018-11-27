from django.contrib.auth.models import User
from rest_framework import filters, viewsets
from django_filters import rest_framework as django_filters, FilterSet
from apps.api import serializers
from apps.projects.models import Theme, DocumentType, Document, Excerpt
from apps.participations.models import InvitedGroup, Suggestion, OpinionVote

DATE_LOOKUPS = ['lt', 'lte', 'gt', 'gte']


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


class ExcerptViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Excerpt.objects.all()
    serializer_class = serializers.ExcerptSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_fields = ('id', 'document__id', 'parent__id', 'excerpt_type')
    search_fields = ('excerpt_type', 'number', 'content')
    ordering_fields = '__all__'


class InvitedGroupFilter(FilterSet):
    class Meta:
        model = InvitedGroup
        fields = {
            'created': DATE_LOOKUPS,
            'modified': DATE_LOOKUPS,
            'closing_date': DATE_LOOKUPS,
            'id': ['exact'],
            'document__title': ['exact', 'contains'],
            'document__description': ['exact', 'contains'],
        }


class InvitedGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InvitedGroup.objects.filter(public_participation=True)
    serializer_class = serializers.InvitedGroupSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = InvitedGroupFilter
    search_fields = ('document__title', 'document__description')
    ordering_fields = '__all__'


class SuggestionFilter(FilterSet):
    class Meta:
        model = Suggestion
        fields = {
            'created': DATE_LOOKUPS,
            'modified': DATE_LOOKUPS,
            'id': ['exact'],
            'excerpt__id': ['exact'],
            'author__id': ['exact'],
        }


class SuggestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Suggestion.objects.all()
    serializer_class = serializers.SuggestionSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = SuggestionFilter
    search_fields = ('content',)
    ordering_fields = '__all__'


class OpinionVoteFilter(FilterSet):
    class Meta:
        model = OpinionVote
        fields = {
            'created': DATE_LOOKUPS,
            'modified': DATE_LOOKUPS,
            'id': ['exact'],
            'owner__id': ['exact'],
            'suggestion__id': ['exact'],
            'opinion_vote': ['exact'],
        }


class OpinionVoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OpinionVote.objects.all()
    serializer_class = serializers.OpinionVoteSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = OpinionVoteFilter
    search_fields = ('content',)
    ordering_fields = '__all__'
