# Generated by Django 2.2 on 2019-05-29 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('participations', '0014_invitedgroup_openning_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitedgroup',
            name='clusters',
        ),
    ]
