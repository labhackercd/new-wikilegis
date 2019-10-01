from django.utils.translation import ugettext_lazy as _
from apps.projects import models, camara_deputados
from wikilegis import celery_app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def create_first_version(sender, instance, created, **kwargs):
    if instance.versions.count() == 0:
        models.DocumentVersion.objects.create(
            document=instance,
            number=0
        )


@celery_app.task
def update_document_infos():
    documents = models.Document.objects.filter(
        document_type__isnull=False,
        number__isnull=False,
        year__isnull=False
    )

    for document in documents:
        success = 0
        try:
            camara_deputados.create_document_info(document)
            success += 1
        except camara_deputados.ProposalNotFound:
            logger.error(
                _('Document "{}" not found on Câmara dos Deputados '
                    'API.'.format(document.title)))

    return _('{} document(s) informations was fetched '
             'successfully.'.format(success))
