# Generated by Django 4.2.3 on 2023-08-29 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_remove_blogpost_likes_count_remove_like_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='post',
        ),
    ]