# Generated by Django 4.2.7 on 2024-05-04 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0003_rename_send_id_messageblock_req_id_and_more'),
        ('report', '0006_alter_report_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='message.message'),
        ),
    ]
