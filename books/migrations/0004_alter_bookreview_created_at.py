# Generated by Django 4.0.1 on 2022-01-30 20:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_bookreview_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
