# Generated by Django 2.1.7 on 2019-02-26 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participations', '0008_auto_20181213_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitedgroup',
            name='clusters',
            field=models.TextField(blank=True, null=True),
        ),
    ]
