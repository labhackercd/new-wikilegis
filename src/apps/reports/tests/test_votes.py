import pytest
from mixer.backend.django import mixer
from apps.reports.models import VotesReport
from apps.reports.tasks import (create_votes_object,
                                get_votes_daily,
                                get_votes_monthly,
                                get_votes_yearly)
from django.db import IntegrityError
from django.urls import reverse
import json
from rest_framework.test import APIClient
import calendar
from apps.participations.models import InvitedGroup, Suggestion, OpinionVote
from apps.projects.models import Document, DocumentVersion, Excerpt
from datetime import date, datetime, timedelta


class TestVotesReport():
    @pytest.mark.django_db
    def test_votes_create(self):
        votes = mixer.blend(VotesReport)
        assert VotesReport.objects.count() == 1
        assert votes.__str__() == ('{} - {}').format(
            votes.start_date.strftime("%d/%m/%Y"), votes.period)

    @pytest.mark.django_db
    def test_votes_integrity_error(self):
        content = mixer.blend(VotesReport)
        with pytest.raises(IntegrityError) as excinfo:
            mixer.blend(VotesReport,
                        period=content.period,
                        start_date=content.start_date)
        assert 'UNIQUE constraint failed' in str(
            excinfo.value)
        ## PostgreSQL message error
        # assert 'duplicate key value violates unique constraint' in str(
        #     excinfo.value)

    @pytest.mark.django_db
    def test_votes_api_url(api_client):
        mixer.cycle(5).blend(VotesReport)
        url = reverse('votesreport-list')
        client = APIClient()
        response = client.get(url)
        request = json.loads(response.content)

        assert response.status_code == 200
        assert request['count'] == 5

    def test_create_votes_daily(self):
        data_daily = ['2020-11-23', 10]
        votes_object = create_votes_object(data_daily, 'daily')

        assert votes_object.period == 'daily'
        assert votes_object.start_date == '2020-11-23'
        assert votes_object.end_date == '2020-11-23'
        assert votes_object.votes == 10

    @pytest.mark.django_db
    def test_create_votes_monthly(self):
        data_monthly = {
            'month': date(2020, 1, 1),
            'total_votes': 10
        }

        votes_object = create_votes_object(data_monthly, 'monthly')

        assert votes_object.period == 'monthly'
        assert votes_object.start_date == date(2020, 1, 1)
        assert votes_object.end_date == date(2020, 1, 31)
        assert votes_object.votes == 10

    @pytest.mark.django_db
    def test_create_votes_yearly(self):
        data_yearly = {
            'year': date(2019, 1, 1),
            'total_votes': 10
        }

        votes_object = create_votes_object(data_yearly, 'yearly')

        assert votes_object.period == 'yearly'
        assert votes_object.start_date == date(2019, 1, 1)
        assert votes_object.end_date == date(2019, 12, 31)
        assert votes_object.votes == 10

    @pytest.mark.django_db(transaction=True)
    def test_get_votes_daily_without_args(self):
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

        vote = mixer.blend(OpinionVote, suggestion=suggestion)
        vote.created = yesterday
        vote.save()

        get_votes_daily.apply()

        daily_data = VotesReport.objects.filter(
            period='daily').first()

        assert daily_data.start_date == yesterday.date()
        assert daily_data.end_date == yesterday.date()
        assert daily_data.period == 'daily'
        assert daily_data.votes == 1

    @pytest.mark.django_db
    def test_get_votes_monthly_without_args(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(VotesReport, period='daily', votes=10,
                    start_date=yesterday, end_date=yesterday)

        get_votes_monthly.apply()

        monthly_data = VotesReport.objects.filter(
            period='monthly').first()

        assert monthly_data.start_date == yesterday.replace(day=1)
        assert monthly_data.end_date == yesterday
        assert monthly_data.period == 'monthly'
        assert monthly_data.votes == 10

    @pytest.mark.django_db
    def test_get_votes_yearly_without_args(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(VotesReport, period='monthly', votes=10,
                    start_date=yesterday.replace(day=1),
                    end_date=yesterday)

        get_votes_yearly.apply()

        yearly_data = VotesReport.objects.filter(period='yearly').first()

        assert yearly_data.start_date == yesterday.replace(day=1, month=1)
        assert yearly_data.end_date == yesterday
        assert yearly_data.period == 'yearly'
        assert yearly_data.votes == 10

    @pytest.mark.django_db
    def test_get_votes_yearly_current_year(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(VotesReport, period='monthly', votes=10,
                    start_date=yesterday.replace(day=1),
                    end_date=yesterday)
        mixer.blend(VotesReport, period='yearly', votes=9,
                    start_date=yesterday.replace(day=1, month=1),
                    end_date=yesterday - timedelta(days=1))

        get_votes_yearly.apply()

        yearly_data = VotesReport.objects.filter(period='yearly').first()

        assert yearly_data.start_date == yesterday.replace(day=1, month=1)
        assert yearly_data.end_date == yesterday
        assert yearly_data.period == 'yearly'
        assert yearly_data.votes == 10
