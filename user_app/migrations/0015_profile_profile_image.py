# Generated by Django 4.2.5 on 2023-09-30 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0014_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
