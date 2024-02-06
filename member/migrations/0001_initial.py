# Generated by Django 4.2.7 on 2024-02-06 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('dormitory_code', models.CharField(max_length=255)),
                ('nickname', models.CharField(max_length=10, unique=True)),
                ('phone_number', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('birthday', models.CharField(max_length=255)),
                ('dormitory_card', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('ADMIN_VERIFICATION_PENDING', '관리자 확인 대기'), ('ACTIVE', '활동'), ('BANNED', '정지'), ('WITHDRAWAL', '탈퇴')], default='ADMIN_VERIFICATION_PENDING', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'member',
            },
        ),
    ]
