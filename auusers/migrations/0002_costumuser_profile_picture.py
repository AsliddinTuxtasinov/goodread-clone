# Generated by Django 4.0.1 on 2022-01-28 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auusers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='costumuser',
            name='profile_picture',
            field=models.ImageField(default='default_profile_pic.jpg', upload_to=''),
        ),
    ]
