# Generated by Django 4.0.1 on 2022-01-30 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auusers', '0002_costumuser_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costumuser',
            name='profile_picture',
            field=models.ImageField(default='default-profile-picture.png', upload_to=''),
        ),
    ]
