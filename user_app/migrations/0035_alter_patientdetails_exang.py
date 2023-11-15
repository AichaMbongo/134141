# Generated by Django 4.2.5 on 2023-10-24 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0034_alter_patientdetails_exang'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdetails',
            name='exang',
            field=models.BooleanField(blank=True, choices=[('0', 'Absence'), ('1', 'Presence')], max_length=1, null=True),
        ),
    ]