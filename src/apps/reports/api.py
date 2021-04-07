from django_filters import FilterSet
from django_filters import rest_framework as django_filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from apps.reports.models import (NewUsersReport, VotesReport, OpinionsReport,
                                 DocumentsReport, ParticipantsReport)
from apps.participations.models import InvitedGroup
from apps.reports.serializers import (NewUsersSerializer,
                                      VotesReportSerializer,
                                      OpinionsReportSerializer,
                                      DocumentsReportSerializer,
                                      ParticipantsReportSerializer,
                                      PublicGroupRankingSerializer)
from django.contrib.sites.models import Site
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class NewUsersFilter(FilterSet):
    class Meta:
        model = NewUsersReport
        fields = {
            'start_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'end_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'period': ['exact'],
        }


class NewUsersViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = NewUsersReport.objects.all()
    serializer_class = NewUsersSerializer
    filter_class = NewUsersFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter
    )
    ordering_fields = '__all__'

    @method_decorator(cache_page(1))  # 1 minute
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['sum_total_results'] = sum([data.get('new_users', 0)
            for data in response.data['results']])
        return response


class VotesReportFilter(FilterSet):
    class Meta:
        model = VotesReport
        fields = {
            'start_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'end_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'period': ['exact'],
        }


class VotesReportViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = VotesReport.objects.all()
    serializer_class = VotesReportSerializer
    filter_class = VotesReportFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter
    )
    ordering_fields = '__all__'

    @method_decorator(cache_page(1))  # 1 minute
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['sum_total_results'] = sum([data.get('votes', 0)
            for data in response.data['results']])
        return response


class OpinionsReportFilter(FilterSet):
    class Meta:
        model = OpinionsReport
        fields = {
            'start_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'end_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'period': ['exact'],
        }


class OpinionsReportViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = OpinionsReport.objects.all()
    serializer_class = OpinionsReportSerializer
    filter_class = OpinionsReportFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter
    )
    ordering_fields = '__all__'

    @method_decorator(cache_page(1))  # 1 minute
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['sum_total_results'] = sum([data.get('opinions', 0)
            for data in response.data['results']])
        return response


class DocumentsReportFilter(FilterSet):
    class Meta:
        model = DocumentsReport
        fields = {
            'start_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'end_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'period': ['exact'],
        }


class DocumentsReportViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = DocumentsReport.objects.all()
    serializer_class = DocumentsReportSerializer
    filter_class = DocumentsReportFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter
    )
    ordering_fields = '__all__'

    @method_decorator(cache_page(1))  # 1 minute
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['sum_total_results'] = sum([data.get('documents', 0)
            for data in response.data['results']])
        return response


class ParticipantsReportFilter(FilterSet):
    class Meta:
        model = ParticipantsReport
        fields = {
            'start_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'end_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'period': ['exact'],
        }


class ParticipantsReportViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = ParticipantsReport.objects.all()
    serializer_class = ParticipantsReportSerializer
    filter_class = ParticipantsReportFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter
    )
    ordering_fields = '__all__'

    @method_decorator(cache_page(1))  # 1 minute
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['sum_total_results'] = sum([data.get('participants', 0)
            for data in response.data['results']])
        return response


class PublicGroupRankingFilter(FilterSet):
    class Meta:
        model = InvitedGroup
        fields = {
            'openning_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'closing_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'group_status': ['exact'],
            'document__themes__name': ['exact'],
        }


class PublicGroupRankingViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = InvitedGroup.objects.filter(
        public_participation=True,
        group_status__in=[
            'finished', 'waiting_feedback', 'analyzing', 'in_progress'])
    serializer_class = PublicGroupRankingSerializer
    pagination_class = LimitOffsetPagination
    filter_class = PublicGroupRankingFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    )
    search_fields = ('document__title', 'document__description')
    ordering_fields = ('openning_date', 'closing_date', 'group_status')

    @method_decorator(cache_page(1)) # 1 minute
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@api_view(['GET'])
def api_reports_root(request, format=None):
    current_site = Site.objects.get_current()
    current_site.domain
    request.META['HTTP_HOST'] = current_site.domain

    return Response({
        'newusers': reverse('newusersreport-list',
                            request=request, format=format),
        'votes': reverse('votesreport-list',
                         request=request, format=format),
        'opinions': reverse('opinionsreport-list',
                         request=request, format=format),
        'documents': reverse('documentsreport-list',
                             request=request, format=format),
        'participants': reverse('participantsreport-list',
                                request=request, format=format),
        'ranking': reverse('ranking-list',
                           request=request, format=format),
    })
