# Generated by Django 2.2 on 2019-05-14 15:50

from django.db import migrations, models
import django.db.models.deletion


def set_default_version(apps, schema_editor):
    InvitedGroup = apps.get_model('participations', 'InvitedGroup')

    for group in InvitedGroup.objects.all():
        last_version = group.document.versions.first()
        group.version = last_version
        group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('participations', '0012_invitedgroup_group_status'),
        ('projects', '0014_auto_20190509_1429')
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitedgroup',
            name='version',
        ),
        migrations.AddField(
            model_name='invitedgroup',
            name='version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invited_groups', to='projects.DocumentVersion', verbose_name='version', null=True),
        ),
        migrations.RunPython(
            set_default_version
        ),
        migrations.AlterField(
            model_name='invitedgroup',
            name='version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invited_groups', to='projects.DocumentVersion', verbose_name='version'),
        ),
        migrations.DeleteModel(
            name='Amendment',
        ),
    ]
