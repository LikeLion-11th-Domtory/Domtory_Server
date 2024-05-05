# Generated by Django 4.2.7 on 2024-05-05 07:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('message', '0003_rename_send_id_messageblock_req_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='recv_id',
        ),
        migrations.RemoveField(
            model_name='message',
            name='send_id',
        ),
        migrations.RemoveField(
            model_name='messageblock',
            name='req_id',
        ),
        migrations.RemoveField(
            model_name='messageblock',
            name='tar_id',
        ),
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_receiver', to=settings.AUTH_USER_MODEL, verbose_name='수신자'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_sender', to=settings.AUTH_USER_MODEL, verbose_name='송신자'),
        ),
        migrations.AddField(
            model_name='messageblock',
            name='requester',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='block_sender', to=settings.AUTH_USER_MODEL, verbose_name='발신자'),
        ),
        migrations.AddField(
            model_name='messageblock',
            name='target',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='block_receiver', to=settings.AUTH_USER_MODEL, verbose_name='수신자'),
        ),
    ]
