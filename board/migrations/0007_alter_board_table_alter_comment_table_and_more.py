# Generated by Django 4.2.7 on 2024-02-11 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0006_alter_comment_is_blocked_alter_comment_is_deleted_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='board',
            table='board',
        ),
        migrations.AlterModelTable(
            name='comment',
            table='comment',
        ),
        migrations.AlterModelTable(
            name='post',
            table='post',
        ),
        migrations.AlterModelTable(
            name='postimage',
            table='postImage',
        ),
    ]
