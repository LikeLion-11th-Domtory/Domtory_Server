# Generated by Django 4.2.7 on 2024-02-19 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0006_member_groups_member_user_permissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='last_login',
        ),
    ]