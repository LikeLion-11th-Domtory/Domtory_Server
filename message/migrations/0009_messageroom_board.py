# Generated by Django 4.2.7 on 2024-05-23 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0008_messageroom_post_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='messageroom',
            name='board',
            field=models.CharField(default='', max_length=60, verbose_name='쪽지 시작점 게시글의 게시판'),
        ),
    ]
