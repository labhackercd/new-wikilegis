import pytest
from mixer.backend.django import mixer
from apps.reports.models import OpinionsReport
from apps.reports.tasks import (create_opinions_object,
                                get_opinions_daily,
                                get_opinions_monthly,
                                get_opinions_yearly)
from django.db import IntegrityError
from django.urls import reverse
import json
from rest_framework.test import APIClient
from datetime import date, datetime, timedelta
import calendar
from apps.participations.models import InvitedGroup, Suggestion
from apps.projects.models import Document, DocumentVersion, Excerpt


class TestOpinionsReport():
    @pytest.mark.django_db
    def test_opinions_create(self):
        opinions = mixer.blend(OpinionsReport)
        assert OpinionsReport.objects.count() == 1
        assert opinions.__str__() == ('{} - {}').format(
            opinions.start_date.strftime("%d/%m/%Y"), opinions.period)

    @pytest.mark.django_db
    def test_opinions_integrity_error(self):
        content = mixer.blend(OpinionsReport)
        with pytest.raises(IntegrityError) as excinfo:
            mixer.blend(OpinionsReport,
                        period=content.period,
                        start_date=content.start_date)
        assert 'UNIQUE constraint failed' in str(
            excinfo.value)
        ## PostgreSQL message error
        # assert 'duplicate key value violates unique constraint' in str(
        #     excinfo.value)

    @pytest.mark.django_db
    def test_opinions_api_url(api_client):
        mixer.cycle(5).blend(OpinionsReport)
        url = reverse('opinionsreport-list')
        client = APIClient()
        response = client.get(url)
        request = json.loads(response.content)

        assert response.status_code == 200
        assert request['count'] == 5

    def test_create_opinions_daily(self):
        data_daily = ['2020-11-23', 10]
        opinions_object = create_opinions_object(data_daily, 'daily')

        assert opinions_object.period == 'daily'
        assert opinions_object.start_date == '2020-11-23'
        assert opinions_object.end_date == '2020-11-23'
        assert opinions_object.opinions == 10

    @pytest.mark.django_db
    def test_create_opinions_monthly(self):
        data_monthly = {
            'month': date(2020, 1, 1),
            'total_opinions': 10
        }

        opinions_object = create_opinions_object(data_monthly, 'monthly')

        assert opinions_object.period == 'monthly'
        assert opinions_object.start_date == date(2020, 1, 1)
        assert opinions_object.end_date == date(2020, 1, 31)
        assert opinions_object.opinions == 10

    @pytest.mark.django_db
    def test_create_opinions_yearly(self):
        data_yearly = {
            'year': date(2019, 1, 1),
            'total_opinions': 10
        }

        opinions_object = create_opinions_object(data_yearly, 'yearly')

        assert opinions_object.period == 'yearly'
        assert opinions_object.start_date == date(2019, 1, 1)
        assert opinions_object.end_date == date(2019, 12, 31)
        assert opinions_object.opinions == 10

    @pytest.mark.django_db(transaction=True)
    def test_get_opinions_daily_without_args(self):
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

        get_opinions_daily.apply()

        daily_data = OpinionsReport.objects.filter(
            period='daily').first()

        assert daily_data.start_date == yesterday.date()
        assert daily_data.end_date == yesterday.date()
        assert daily_data.period == 'daily'
        assert daily_data.opinions == 1

    @pytest.mark.django_db
    def test_get_opinions_monthly_with_args(self):
        mixer.cycle(5).blend(OpinionsReport, period='daily',
                             opinions=10, start_date=mixer.sequence(
                                 '2020-10-1{0}'),
                             end_date=mixer.sequence('2020-10-1{0}'))

        get_opinions_monthly.apply(args=(['2020-10-01']))

        monthly_data = OpinionsReport.objects.filter(
            period='monthly').first()

        assert monthly_data.start_date == date(2020, 10, 1)
        assert monthly_data.end_date == date(2020, 10, 31)
        assert monthly_data.period == 'monthly'
        assert monthly_data.opinions == 50

    @pytest.mark.django_db
    def test_get_opinions_monthly_without_args(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(OpinionsReport, period='daily', opinions=10,
                    start_date=yesterday, end_date=yesterday)

        get_opinions_monthly.apply()

        monthly_data = OpinionsReport.objects.filter(
            period='monthly').first()

        assert monthly_data.start_date == yesterday.replace(day=1)
        assert monthly_data.end_date == yesterday
        assert monthly_data.period == 'monthly'
        assert monthly_data.opinions == 10

    @pytest.mark.django_db
    def test_get_opinions_yearly_with_args(self):
        start_dates = ['2019-01-01', '2019-02-01', '2019-03-01']
        end_dates = ['2019-01-31', '2019-02-28', '2019-03-31']
        for i in range(3):
            mixer.blend(OpinionsReport, period='monthly', opinions=10,
                        start_date=start_dates[i], end_date=end_dates[i])

        get_opinions_yearly.apply(args=(['2019-01-01']))

        yearly_data = OpinionsReport.objects.filter(
            period='yearly').first()

        assert yearly_data.start_date == date(2019, 1, 1)
        assert yearly_data.end_date == date(2019, 12, 31)
        assert yearly_data.period == 'yearly'
        assert yearly_data.opinions == 30

    @pytest.mark.django_db
    def test_get_opinions_yearly_without_args(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(OpinionsReport, period='monthly', opinions=10,
                    start_date=yesterday.replace(day=1),
                    end_date=yesterday)

        get_opinions_yearly.apply()

        yearly_data = OpinionsReport.objects.filter(period='yearly').first()

        assert yearly_data.start_date == yesterday.replace(day=1, month=1)
        assert yearly_data.end_date == yesterday
        assert yearly_data.period == 'yearly'
        assert yearly_data.opinions == 10

    @pytest.mark.django_db
    def test_get_opinions_yearly_current_year(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(OpinionsReport, period='monthly', opinions=10,
                    start_date=yesterday.replace(day=1),
                    end_date=yesterday)
        mixer.blend(OpinionsReport, period='yearly', opinions=9,
                    start_date=yesterday.replace(day=1, month=1),
                    end_date=yesterday - timedelta(days=1))

        get_opinions_yearly.apply()

        yearly_data = OpinionsReport.objects.filter(period='yearly').first()

        assert yearly_data.start_date == yesterday.replace(day=1, month=1)
        assert yearly_data.end_date == yesterday
        assert yearly_data.period == 'yearly'
        assert yearly_data.opinions == 10
