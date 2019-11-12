from django.contrib.auth.models import User
from rest_framework import filters, viewsets
from django_filters import rest_framework as django_filters, FilterSet
from apps.api import serializers
from apps.projects.models import Theme, DocumentType, Document, Excerpt
from apps.participations.models import InvitedGroup, Suggestion, OpinionVote
from apps.accounts.models import ThematicGroup
from django.contrib.sites.models import Site

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


class UserViewSet(viewsets.ModelViewSet):
    allowed_methods = ['get', 'put', 'delete']
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
    )
    filter_class = UserFilter
    search_fields = ('username', 'first_name', 'last_name')
    ordering_fields = '__all__'

    def get_serializer_context(self):
        current_site = Site.objects.get_current()
        current_site.domain
        self.request.META['HTTP_HOST'] = current_site.domain
        return {'request': self.request}


class ThemeFilter(FilterSet):
    class Meta:
        model = Theme
        fields = {
            'id': ['exact'],
            'name': ['exact', 'contains', 'icontains'],
            'slug': ['exact', 'contains', 'icontains'],
        }


class ThemeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = serializers.ThemeSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = ThemeFilter
    search_fields = ('name', 'slug')
    ordering_fields = '__all__'
    ordering = ('name',)

    def get_serializer_context(self):
        current_site = Site.objects.get_current()
        current_site.domain
        self.request.META['HTTP_HOST'] = current_site.domain
        return {'request': self.request}


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

    def get_serializer_context(self):
        current_site = Site.objects.get_current()
        current_site.domain
        self.request.META['HTTP_HOST'] = current_site.domain
        return {'request': self.request}


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Document.objects.filter(
        invited_groups__public_participation=True,
        invited_groups__group_status='in_progress')
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

    def get_serializer_context(self):
        current_site = Site.objects.get_current()
        current_site.domain
        self.request.META['HTTP_HOST'] = current_site.domain
        return {'request': self.request}


class ExcerptViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Excerpt.objects.all()
    serializer_class = serializers.ExcerptSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_fields = ('id', 'document__id', 'excerpt_type')
    search_fields = ('excerpt_type', 'number', 'content')
    ordering_fields = '__all__'

    def get_serializer_context(self):
        current_site = Site.objects.get_current()
        current_site.domain
        self.request.META['HTTP_HOST'] = current_site.domain
        return {'request': self.request}


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
    queryset = InvitedGroup.objects.filter(
        public_participation=True,
        group_status='in_progress').order_by('-closing_date')
    serializer_class = serializers.InvitedGroupSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = InvitedGroupFilter
    search_fields = ('document__title', 'document__description')
    ordering_fields = '__all__'

    def get_serializer_context(self):
        current_site = Site.objects.get_current()
        current_site.domain
        self.request.META['HTTP_HOST'] = current_site.domain
        return {'request': self.request}


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

    def get_serializer_context(self):
        current_site = Site.objects.get_current()
        current_site.domain
        self.request.META['HTTP_HOST'] = current_site.domain
        return {'request': self.request}


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

    def get_serializer_context(self):
        current_site = Site.objects.get_current()
        current_site.domain
        self.request.META['HTTP_HOST'] = current_site.domain
        return {'request': self.request}


class ThematicGroupFilter(FilterSet):
    class Meta:
        model = ThematicGroup
        fields = {
            'id': ['exact'],
            'name': ['exact', 'contains', 'icontains']
        }


class ThematicGroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ThematicGroupSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = ThematicGroupFilter
    search_fields = ('name',)
    ordering_fields = '__all__'
    queryset = ThematicGroup.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.owner_groups.all()
        else:
            return ThematicGroup.objects.none()

    def get_serializer_context(self):
        current_site = Site.objects.get_current()
        current_site.domain
        self.request.META['HTTP_HOST'] = current_site.domain
        return {'request': self.request}
