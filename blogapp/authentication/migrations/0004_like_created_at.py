# Generated by Django 4.2.3 on 2023-08-28 11:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
