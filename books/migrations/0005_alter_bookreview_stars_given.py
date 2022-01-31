# Generated by Django 4.0.1 on 2022-01-31 19:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_bookreview_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='stars_given',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]