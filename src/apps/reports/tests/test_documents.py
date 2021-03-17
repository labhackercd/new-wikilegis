import pytest
from mixer.backend.django import mixer
from apps.reports.models import DocumentsReport
from django.db import IntegrityError
from django.urls import reverse
import json
from rest_framework.test import APIClient
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
