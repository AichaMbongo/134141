# Generated by Django 4.2.5 on 2023-11-14 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0050_alter_predictionresult_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientdetails',
            name='neg',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
