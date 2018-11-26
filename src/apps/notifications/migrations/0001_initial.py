# Generated by Django 2.1.3 on 2018-11-21 12:59

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('participations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvitedEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('email', models.EmailField(max_length=254)),
                ('hash_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('accepted', models.BooleanField(default=False, verbose_name='accepted')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invited_emails', to='participations.InvitedGroup', verbose_name='group')),
            ],
            options={
                'verbose_name': 'invited email',
                'verbose_name_plural': 'invited emails',
            },
        ),
        migrations.AlterUniqueTogether(
            name='invitedemail',
            unique_together={('email', 'group')},
        ),
    ]