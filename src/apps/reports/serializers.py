from rest_framework import serializers
from apps.reports.models import (NewUsersReport, VotesReport, OpinionsReport,
                                 DocumentsReport, ParticipantsReport)


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
