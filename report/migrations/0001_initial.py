# Generated by Django 4.2.7 on 2024-02-11 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('board', '0006_alter_comment_is_blocked_alter_comment_is_deleted_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('WAITING', '대기'), ('PENDING', '수동검사대기'), ('VALID', '욕설있음'), ('INVALID', '욕설없음')], default='WAITING', max_length=10)),
                ('reported_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(default='댓글 없음(삭제됨)', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='board.comment')),
                ('post', models.ForeignKey(default='게시글 없음(삭제됨)', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='board.post')),
            ],
        ),
    ]