# Generated by Django 4.2.5 on 2023-11-04 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0042_profile_on_leave'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='treats',
        ),
    ]
