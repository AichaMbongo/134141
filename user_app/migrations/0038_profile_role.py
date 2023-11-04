# Generated by Django 4.2.5 on 2023-11-04 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0037_alter_patientdetails_exang'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('secretary', 'Secretary'), ('nurse', 'Nurse'), ('doctor', 'Doctor'), ('unassigned', 'Unassigned')], default='unassigned', max_length=12),
        ),
    ]
