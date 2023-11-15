# Generated by Django 4.2.5 on 2023-11-04 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0039_remove_profile_role_customuser_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='role',
        ),
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('secretary', 'Secretary'), ('nurse', 'Nurse'), ('doctor', 'Doctor'), ('unassigned', 'Unassigned')], default='unassigned', max_length=12),
        ),
    ]