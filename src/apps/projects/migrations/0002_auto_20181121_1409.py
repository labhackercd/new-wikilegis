# Generated by Django 2.1.3 on 2018-11-21 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='theme',
        ),
        migrations.AddField(
            model_name='document',
            name='themes',
            field=models.ManyToManyField(to='projects.Theme', verbose_name='themes'),
        ),
    ]