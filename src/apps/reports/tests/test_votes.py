import pytest
from mixer.backend.django import mixer
from apps.reports.models import VotesReport
from django.db import IntegrityError
from django.urls import reverse
import json
from rest_framework.test import APIClient
import calendar


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
