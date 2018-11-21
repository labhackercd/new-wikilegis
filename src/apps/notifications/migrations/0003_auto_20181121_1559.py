# Generated by Django 2.1.3 on 2018-11-21 17:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20181121_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='OwnerInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('email', models.EmailField(max_length=254)),
                ('hash_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('accepted', models.BooleanField(default=False, verbose_name='accepted')),
            ],
            options={
                'verbose_name': 'owner invitation',
                'verbose_name_plural': 'owner invitations',
            },
        ),
        migrations.AlterModelOptions(
            name='parcipantinvitation',
            options={'verbose_name': 'participant invitation', 'verbose_name_plural': 'participant invitations'},
        ),
    ]
