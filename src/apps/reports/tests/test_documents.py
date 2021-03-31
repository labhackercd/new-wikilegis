import pytest
from mixer.backend.django import mixer
from apps.reports.models import DocumentsReport
from apps.reports.tasks import (create_documents_object,
                                get_documents_daily,
                                get_documents_monthly,
                                get_documents_yearly)
from django.db import IntegrityError
from django.urls import reverse
from rest_framework.test import APIClient
from apps.participations.models import InvitedGroup
from apps.projects.models import Document, DocumentVersion
from datetime import date, datetime, timedelta
import json
import calendar


class TestDocumentsReport():
    @pytest.mark.django_db
    def test_documents_create(self):
        documents = mixer.blend(DocumentsReport)
        assert DocumentsReport.objects.count() == 1
        assert documents.__str__() == ('{} - {}').format(
            documents.start_date.strftime("%d/%m/%Y"), documents.period)

    @pytest.mark.django_db
    def test_documents_integrity_error(self):
        content = mixer.blend(DocumentsReport)
        with pytest.raises(IntegrityError) as excinfo:
            mixer.blend(DocumentsReport,
                        period=content.period,
                        start_date=content.start_date)
        assert 'UNIQUE constraint failed' in str(
            excinfo.value)
        ## PostgreSQL message error
        # assert 'duplicate key value violates unique constraint' in str(
        #     excinfo.value)

    @pytest.mark.django_db
    def test_documents_api_url(api_client):
        mixer.cycle(5).blend(DocumentsReport)
        url = reverse('documentsreport-list')
        client = APIClient()
        response = client.get(url)
        request = json.loads(response.content)

        assert response.status_code == 200
        assert request['count'] == 5

    def test_create_documents_daily(self):
        data_daily = ['2020-11-23', 10]
        documents_object = create_documents_object(data_daily, 'daily')

        assert documents_object.period == 'daily'
        assert documents_object.start_date == '2020-11-23'
        assert documents_object.end_date == '2020-11-23'
        assert documents_object.documents == 10

    @pytest.mark.django_db
    def test_create_documents_monthly(self):
        data_monthly = {
            'month': date(2020, 1, 1),
            'total_documents': 10
        }

        documents_object = create_documents_object(data_monthly, 'monthly')

        assert documents_object.period == 'monthly'
        assert documents_object.start_date == date(2020, 1, 1)
        assert documents_object.end_date == date(2020, 1, 31)
        assert documents_object.documents == 10

    @pytest.mark.django_db
    def test_create_documents_yearly(self):
        data_yearly = {
            'year': date(2019, 1, 1),
            'total_documents': 10
        }

        documents_object = create_documents_object(data_yearly, 'yearly')

        assert documents_object.period == 'yearly'
        assert documents_object.start_date == date(2019, 1, 1)
        assert documents_object.end_date == date(2019, 12, 31)
        assert documents_object.documents == 10

    @pytest.mark.django_db(transaction=True)
    def test_get_documents_daily_without_args(self):
        yesterday = datetime.now() - timedelta(days=1)

        document = mixer.blend(Document)
        document_version = mixer.blend(DocumentVersion, document=document,
            number=1, auto_save=False, parent=None)

        public_group = mixer.blend(InvitedGroup, document=document,
            version=document_version, public_participation=True)
        public_group.created = yesterday
        public_group.group_status = 'in_progress'
        public_group.save()

        get_documents_daily.apply()

        daily_data = DocumentsReport.objects.filter(
            period='daily').first()

        assert daily_data.start_date == yesterday.date()
        assert daily_data.end_date == yesterday.date()
        assert daily_data.period == 'daily'
        assert daily_data.documents == 1

    @pytest.mark.django_db
    def test_get_documents_monthly_with_args(self):
        mixer.cycle(5).blend(DocumentsReport, period='daily',
                             documents=10, start_date=mixer.sequence(
                                 '2020-10-1{0}'),
                             end_date=mixer.sequence('2020-10-1{0}'))

        get_documents_monthly.apply(args=(['2020-10-01']))

        monthly_data = DocumentsReport.objects.filter(
            period='monthly').first()

        assert monthly_data.start_date == date(2020, 10, 1)
        assert monthly_data.end_date == date(2020, 10, 31)
        assert monthly_data.period == 'monthly'
        assert monthly_data.documents == 50

    @pytest.mark.django_db
    def test_get_documents_monthly_without_args(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(DocumentsReport, period='daily', documents=10,
                    start_date=yesterday, end_date=yesterday)

        get_documents_monthly.apply()

        monthly_data = DocumentsReport.objects.filter(
            period='monthly').first()

        assert monthly_data.start_date == yesterday.replace(day=1)
        assert monthly_data.end_date == yesterday
        assert monthly_data.period == 'monthly'
        assert monthly_data.documents == 10

    @pytest.mark.django_db
    def test_get_documents_yearly_with_args(self):
        start_dates = ['2019-01-01', '2019-02-01', '2019-03-01']
        end_dates = ['2019-01-31', '2019-02-28', '2019-03-31']
        for i in range(3):
            mixer.blend(DocumentsReport, period='monthly', documents=10,
                        start_date=start_dates[i], end_date=end_dates[i])

        get_documents_yearly.apply(args=(['2019-01-01']))

        yearly_data = DocumentsReport.objects.filter(
            period='yearly').first()

        assert yearly_data.start_date == date(2019, 1, 1)
        assert yearly_data.end_date == date(2019, 12, 31)
        assert yearly_data.period == 'yearly'
        assert yearly_data.documents == 30

    @pytest.mark.django_db
    def test_get_documents_yearly_without_args(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(DocumentsReport, period='monthly', documents=10,
                    start_date=yesterday.replace(day=1),
                    end_date=yesterday)

        get_documents_yearly.apply()

        yearly_data = DocumentsReport.objects.filter(period='yearly').first()

        assert yearly_data.start_date == yesterday.replace(day=1, month=1)
        assert yearly_data.end_date == yesterday
        assert yearly_data.period == 'yearly'
        assert yearly_data.documents == 10

    @pytest.mark.django_db
    def test_get_documents_yearly_current_year(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(DocumentsReport, period='monthly', documents=10,
                    start_date=yesterday.replace(day=1),
                    end_date=yesterday)
        mixer.blend(DocumentsReport, period='yearly', documents=9,
                    start_date=yesterday.replace(day=1, month=1),
                    end_date=yesterday - timedelta(days=1))

        get_documents_yearly.apply()

        yearly_data = DocumentsReport.objects.filter(period='yearly').first()

        assert yearly_data.start_date == yesterday.replace(day=1, month=1)
        assert yearly_data.end_date == yesterday
        assert yearly_data.period == 'yearly'
        assert yearly_data.documents == 10
