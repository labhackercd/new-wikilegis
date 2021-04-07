import pytest
from mixer.backend.django import mixer
from apps.participations.models import InvitedGroup
from apps.projects.models import Document, DocumentVersion
from django.urls import reverse
import json
from rest_framework.test import APIClient


class TestRankingReport():
    @pytest.mark.django_db
    def test_ranking_api_url(api_client):
        document = mixer.blend(Document)
        document_version = mixer.blend(DocumentVersion, document=document,
            number=1, auto_save=False, parent=None)
        group = mixer.blend(InvitedGroup, document=document,
            version=document_version, public_participation=True)
        group.group_status = 'in_progress'
        group.save()
        url = reverse('ranking-list')
        client = APIClient()
        response = client.get(url)
        request = json.loads(response.content)

        assert response.status_code == 200
        assert request['count'] == 1
