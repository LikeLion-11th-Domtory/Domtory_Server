# Generated by Django 4.2.7 on 2024-02-09 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='parent',
            new_name='parent_id',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='post_id',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='board',
            new_name='board_id',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='member',
            new_name='member_id',
        ),
        migrations.RenameField(
            model_name='postimage',
            old_name='post',
            new_name='post_id',
        ),
    ]
