# Generated by Django 2.1.5 on 2019-05-06 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participations', '0011_auto_20190429_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitedgroup',
            name='group_status',
            field=models.CharField(choices=[('waiting', 'Waiting'), ('in_progress', 'In Progress')], default='in_progress', max_length=200, verbose_name='group status'),
        ),
    ]