# Generated by Django 4.2.7 on 2024-03-05 01:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('push', '0002_rename_last_logged_in_at_device_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminPushNotification',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, help_text='제목을 넣어주세요. ex) 돔토리 업데이트 공지사항', max_length=255)),
                ('body', models.CharField(help_text='본문을 넣어주세요. ex) 1.10 버전이 새로 출시 되었으니 업데이트 바라요!', max_length=255)),
                ('created_at', models.DateTimeField()),
                ('notification_type', models.CharField(choices=[('normal', '일반 공지'), ('update', '업데이트 알림'), ('emergency', '긴급 공지')], max_length=20, null=True)),
                ('staff_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '관리자 푸시 알림',
                'verbose_name_plural': '관리자 푸시 알림',
                'db_table': 'admin_push_notification',
            },
        ),
    ]