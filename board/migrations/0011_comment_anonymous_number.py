# Generated by Django 4.2.7 on 2024-02-19 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0010_alter_board_description_alter_board_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='anonymous_number',
            field=models.IntegerField(default=1),
        ),
    ]
