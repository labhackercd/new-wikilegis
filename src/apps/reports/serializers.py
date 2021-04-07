from rest_framework import serializers
from apps.reports.models import (NewUsersReport, VotesReport, OpinionsReport,
                                 DocumentsReport, ParticipantsReport)
from apps.api.serializers import (DocumentTypeSerializer, ThemeSerializer,
                                  DocumentResponsibleSerializer)
from apps.participations.models import InvitedGroup, OpinionVote
from apps.projects.models import Document
from django.db.models import Count


class NewUsersSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    modified = serializers.DateTimeField(format="%d/%m/%Y %H:%M")

    def get_month(self, obj):
        return obj.start_date.month

    def get_year(self, obj):
        return obj.start_date.year

    class Meta:
        model = NewUsersReport
        fields = ('start_date', 'end_date', 'period', 'new_users', 'month',
                  'year', 'modified')


class VotesReportSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    modified = serializers.DateTimeField(format="%d/%m/%Y %H:%M")

    def get_month(self, obj):
        return obj.start_date.month

    def get_year(self, obj):
        return obj.start_date.year

    class Meta:
        model = VotesReport
        fields = ('start_date', 'end_date', 'period', 'votes', 'month',
                  'year', 'modified')


class OpinionsReportSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    modified = serializers.DateTimeField(format="%d/%m/%Y %H:%M")

    def get_month(self, obj):
        return obj.start_date.month

    def get_year(self, obj):
        return obj.start_date.year

    class Meta:
        model = OpinionsReport
        fields = ('start_date', 'end_date', 'period', 'opinions', 'month',
                  'year', 'modified')


class DocumentsReportSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    modified = serializers.DateTimeField(format="%d/%m/%Y %H:%M")

    def get_month(self, obj):
        return obj.start_date.month

    def get_year(self, obj):
        return obj.start_date.year

    class Meta:
        model = DocumentsReport
        fields = ('start_date', 'end_date', 'period', 'documents', 'month',
                  'year', 'modified')


class ParticipantsReportSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    modified = serializers.DateTimeField(format="%d/%m/%Y %H:%M")

    def get_month(self, obj):
        return obj.start_date.month

    def get_year(self, obj):
        return obj.start_date.year

    class Meta:
        model = ParticipantsReport
        fields = ('start_date', 'end_date', 'period', 'participants', 'month',
                  'year', 'modified')


class DocumentRankingSerializer(serializers.ModelSerializer):
    document_type = DocumentTypeSerializer()
    themes = ThemeSerializer(many=True)
    responsible = DocumentResponsibleSerializer()

    class Meta:
        model = Document
        fields = ('title', 'description', 'document_type',
                  'number', 'year', 'themes', 'responsible')


class PublicGroupRankingSerializer(serializers.ModelSerializer):
    document = DocumentRankingSerializer()
    suggestions_count = serializers.SerializerMethodField()
    vote_count = serializers.SerializerMethodField()
    participants_count = serializers.SerializerMethodField()
    group_status = serializers.CharField(source='get_group_status_display')

    class Meta:
        model = InvitedGroup
        fields = ('document', 'group_status', 'openning_date', 'closing_date',
                  'suggestions_count', 'vote_count', 'participants_count')

    def get_suggestions_count(self, obj):
        return obj.suggestions.count()

    def get_vote_count(self, obj):
        suggestions = obj.suggestions.all()
        total_votes = suggestions.annotate(num_votes=Count(
            'votes')).values_list('num_votes', flat=True)

        return sum(total_votes)

    def get_participants_count(self, obj):
        suggestions = obj.suggestions.all()
        list_user_suggestion = list(
            suggestions.values_list('author__id', flat=True))
        list_id_suggestion = list(suggestions.values_list('id', flat=True))
        list_users_votes = list(OpinionVote.objects.filter(
            suggestion__id__in=list_id_suggestion)
            .values_list('owner__id', flat=True))

        list_user = list(set(list_user_suggestion + list_users_votes))

        return len(list_user)
