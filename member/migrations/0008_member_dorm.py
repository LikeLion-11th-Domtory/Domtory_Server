# Generated by Django 4.2.7 on 2024-07-29 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dorm', '0004_alter_dorm_dorm_name'),
        ('member', '0007_remove_member_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='dorm',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='dorm.dorm', verbose_name='소속 기숙사'),
        ),
    ]