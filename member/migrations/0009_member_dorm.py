# Generated by Django 4.2.7 on 2024-08-31 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dorm', '0004_alter_dorm_dorm_name'),
        ('member', '0008_personalinfoexcelfile_dorm'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='dorm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dorm.dorm'),
        ),
    ]