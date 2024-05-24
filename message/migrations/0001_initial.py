# Generated by Django 4.2.7 on 2024-04-19 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(default='', verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='전송일시')),
                ('is_read', models.BooleanField(default=False)),
                ('is_deleted_send', models.BooleanField(default=False)),
                ('is_deleted_recv', models.BooleanField(default=False)),
                ('recv_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_receiver', to=settings.AUTH_USER_MODEL, verbose_name='수신자')),
                ('send_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_sender', to=settings.AUTH_USER_MODEL, verbose_name='송신자')),
            ],
        ),
    ]
