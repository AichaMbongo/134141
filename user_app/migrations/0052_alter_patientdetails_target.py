# Generated by Django 4.2.5 on 2023-11-13 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0051_heartdiseaseprediction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdetails',
            name='target',
            field=models.CharField(blank=True, choices=[('0', 'False'), ('1', 'True')], max_length=1, null=True),
        ),
    ]
