# Generated by Django 4.2.4 on 2023-08-30 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_rename_parent_comment_commentreply_parent_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
