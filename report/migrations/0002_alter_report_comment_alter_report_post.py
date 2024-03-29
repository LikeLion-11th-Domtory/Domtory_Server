# Generated by Django 4.2.7 on 2024-02-11 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0006_alter_comment_is_blocked_alter_comment_is_deleted_and_more'),
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='board.comment'),
        ),
        migrations.AlterField(
            model_name='report',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='board.post'),
        ),
    ]
