from apps.projects import models


def create_first_version(sender, instance, created, **kwargs):
    if instance.versions.count() == 0:
        models.DocumentVersion.objects.create(
            document=instance,
            number=0
        )
