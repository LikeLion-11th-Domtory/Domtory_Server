# Generated by Django 4.2.7 on 2024-05-16 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0005_messageinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messageinfo',
            name='sender_anonymous_num',
        ),
    ]