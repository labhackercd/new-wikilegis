# Generated by Django 2.2.19 on 2021-08-19 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_feedbackauthorization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackauthorization',
            name='video_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='video id'),
        ),
    ]