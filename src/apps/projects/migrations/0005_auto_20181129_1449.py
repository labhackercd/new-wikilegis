# Generated by Django 2.1.3 on 2018-11-29 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20181129_1433'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='excerpt',
            options={'ordering': ('order', 'id'), 'verbose_name': 'excerpt', 'verbose_name_plural': 'excerpts'},
        ),
    ]
