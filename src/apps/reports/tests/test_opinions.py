import pytest
from mixer.backend.django import mixer
from apps.reports.models import OpinionsReport
from django.db import IntegrityError
from django.urls import reverse
import json
from rest_framework.test import APIClient
import calendar


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
