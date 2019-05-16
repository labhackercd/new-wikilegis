from apps.projects.models import DocumentVersion


def create_named_version(document, name, version):
    if version:
        base_version = document.versions.get(
            number=version
        )
    else:
        base_version = document.versions.first()

    last_named_version = document.versions.filter(
        name__isnull=False,
        auto_save=False
    ).first()

    new_version = DocumentVersion.objects.create(
        number=base_version.number + 1,
        name=name,
        auto_save=False,
        document=document
    )

    for excerpt in base_version.excerpts.all():
        new_excerpt = excerpt
        new_excerpt.pk = None
        new_excerpt.version = new_version
        new_excerpt.save()

    if last_named_version:
        autosaves = document.versions.filter(
            auto_save=True,
            created__gt=last_named_version.created,
            created__lt=new_version.created
        )
    else:
        autosaves = document.versions.filter(
            auto_save=True,
            created__lt=new_version.created
        )

    for version in autosaves:
        version.parent = new_version
        version.save()

    return new_version
