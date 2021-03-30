import pytest
from mixer.backend.django import mixer
from apps.reports.models import ParticipantsReport
from django.db import IntegrityError
from apps.participations.models import InvitedGroup, Suggestion
from apps.projects.models import Document, DocumentVersion, Excerpt
from apps.reports.tasks import (create_participants_object,
                                get_participants_daily,
                                get_participants_monthly,
                                get_participants_yearly)
from datetime import date, datetime, timedelta
from django.urls import reverse
import json
from rest_framework.test import APIClient
import calendar


class TestParticipantsReport():
    @pytest.mark.django_db
    def test_participants_create(self):
        participants = mixer.blend(ParticipantsReport)
        assert ParticipantsReport.objects.count() == 1
        assert participants.__str__() == ('{} - {}').format(
            participants.start_date.strftime("%d/%m/%Y"), participants.period)

    @pytest.mark.django_db
    def test_participants_integrity_error(self):
        content = mixer.blend(ParticipantsReport)
        with pytest.raises(IntegrityError) as excinfo:
            mixer.blend(ParticipantsReport,
                        period=content.period,
                        start_date=content.start_date)
        assert 'UNIQUE constraint failed' in str(
            excinfo.value)
        ## PostgreSQL message error
        # assert 'duplicate key value violates unique constraint' in str(
        #     excinfo.value)

    @pytest.mark.django_db
    def test_participants_api_url(api_client):
        mixer.cycle(5).blend(ParticipantsReport)
        url = reverse('participantsreport-list')
        client = APIClient()
        response = client.get(url)
        request = json.loads(response.content)

        assert response.status_code == 200
        assert request['count'] == 5

    def test_create_participants_daily(self):
        data_daily = ['2020-11-23', 10]
        participants_object = create_participants_object(data_daily, 'daily')

        assert participants_object.period == 'daily'
        assert participants_object.start_date == '2020-11-23'
        assert participants_object.end_date == '2020-11-23'
        assert participants_object.participants == 10

    @pytest.mark.django_db
    def test_create_participants_monthly(self):
        data_monthly = {
            'month': date(2020, 1, 1),
            'total_participants': 10
        }

        participants_object = create_participants_object(data_monthly, 'monthly')

        assert participants_object.period == 'monthly'
        assert participants_object.start_date == date(2020, 1, 1)
        assert participants_object.end_date == date(2020, 1, 31)
        assert participants_object.participants == 10

    @pytest.mark.django_db
    def test_create_participants_yearly(self):
        data_yearly = {
            'year': date(2019, 1, 1),
            'total_participants': 10
        }

        participants_object = create_participants_object(data_yearly, 'yearly')

        assert participants_object.period == 'yearly'
        assert participants_object.start_date == date(2019, 1, 1)
        assert participants_object.end_date == date(2019, 12, 31)
        assert participants_object.participants == 10

    @pytest.mark.django_db(transaction=True)
    def test_get_participants_daily_without_args(self):
        yesterday = datetime.now() - timedelta(days=1)

        document = mixer.blend(Document)
        document_version = mixer.blend(DocumentVersion, document=document,
            number=1, auto_save=False, parent=None)

        public_group = mixer.blend(InvitedGroup, document=document,
            version=document_version, public_participation=True)
        public_group.created = yesterday
        public_group.save()

        excerpt = mixer.blend(Excerpt, document=document,
            version=document_version)
        excerpt.created = yesterday
        excerpt.save()

        suggestion = mixer.blend(Suggestion, invited_group=public_group,
            excerpt=excerpt)
        suggestion.created = yesterday
        suggestion.save()

        get_participants_daily.apply()

        daily_data = ParticipantsReport.objects.filter(
            period='daily').first()

        assert daily_data.start_date == yesterday.date()
        assert daily_data.end_date == yesterday.date()
        assert daily_data.period == 'daily'
        assert daily_data.participants == 1

    @pytest.mark.django_db
    def test_get_participants_monthly_without_args(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(ParticipantsReport, period='daily', participants=10,
                    start_date=yesterday, end_date=yesterday)

        get_participants_monthly.apply()

        monthly_data = ParticipantsReport.objects.filter(
            period='monthly').first()

        assert monthly_data.start_date == yesterday.replace(day=1)
        assert monthly_data.end_date == yesterday
        assert monthly_data.period == 'monthly'
        assert monthly_data.participants == 10

    @pytest.mark.django_db
    def test_get_participants_yearly_without_args(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(ParticipantsReport, period='monthly', participants=10,
                    start_date=yesterday.replace(day=1),
                    end_date=yesterday)

        get_participants_yearly.apply()

        yearly_data = ParticipantsReport.objects.filter(
            period='yearly').first()

        assert yearly_data.start_date == yesterday.replace(day=1, month=1)
        assert yearly_data.end_date == yesterday
        assert yearly_data.period == 'yearly'
        assert yearly_data.participants == 10

    @pytest.mark.django_db
    def test_get_participants_yearly_current_year(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(ParticipantsReport, period='monthly', participants=10,
                    start_date=yesterday.replace(day=1),
                    end_date=yesterday)
        mixer.blend(ParticipantsReport, period='yearly', participants=9,
                    start_date=yesterday.replace(day=1, month=1),
                    end_date=yesterday - timedelta(days=1))

        get_participants_yearly.apply()

        yearly_data = ParticipantsReport.objects.filter(period='yearly').first()

        assert yearly_data.start_date == yesterday.replace(day=1, month=1)
        assert yearly_data.end_date == yesterday
        assert yearly_data.period == 'yearly'
        assert yearly_data.participants == 10
