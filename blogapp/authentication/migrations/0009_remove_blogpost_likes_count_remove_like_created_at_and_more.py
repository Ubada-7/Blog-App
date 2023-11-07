# Generated by Django 4.2.4 on 2023-08-29 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0008_alter_comment_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='likes_count',
        ),
        migrations.RemoveField(
            model_name='like',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]