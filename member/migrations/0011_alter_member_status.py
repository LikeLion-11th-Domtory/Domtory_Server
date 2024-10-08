# Generated by Django 4.2.7 on 2024-09-07 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0010_dormitorypersonalinfo_dorm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.CharField(choices=[('PENDING', '가입 승인 대기'), ('ACTIVE', '활동'), ('BANNED', '정지'), ('WITHDRAWAL', '탈퇴')], default='ACTIVE', max_length=255),
        ),
    ]
