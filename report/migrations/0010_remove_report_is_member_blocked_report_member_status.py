# Generated by Django 4.2.7 on 2024-07-16 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0009_remove_report_member_report_is_member_blocked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='is_member_blocked',
        ),
        migrations.AddField(
            model_name='report',
            name='member_status',
            field=models.CharField(choices=[('BANNED', '유저 정지'), ('ACTIVE', '유저 정지 해제')], default='ACTIVE', max_length=10),
        ),
    ]
