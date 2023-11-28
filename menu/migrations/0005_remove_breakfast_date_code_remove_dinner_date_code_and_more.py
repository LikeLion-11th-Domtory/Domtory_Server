# Generated by Django 4.2.7 on 2023-11-28 01:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0004_alter_breakfast_date_code_alter_dinner_date_code_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="breakfast",
            name="date_code",
        ),
        migrations.RemoveField(
            model_name="dinner",
            name="date_code",
        ),
        migrations.RemoveField(
            model_name="lunch",
            name="date_code",
        ),
        migrations.AddField(
            model_name="breakfast",
            name="name",
            field=models.CharField(default=1, max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="dinner",
            name="name",
            field=models.CharField(default="1234", max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="lunch",
            name="name",
            field=models.CharField(default=3, max_length=512),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="breakfast",
            name="menu",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="breakfasts",
                to="menu.menu",
            ),
        ),
        migrations.AlterField(
            model_name="dinner",
            name="menu",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="dinners",
                to="menu.menu",
            ),
        ),
        migrations.AlterField(
            model_name="lunch",
            name="menu",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lunches",
                to="menu.menu",
            ),
        ),
    ]
