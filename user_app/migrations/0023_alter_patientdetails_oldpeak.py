# Generated by Django 4.2.5 on 2023-10-06 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0022_alter_patientdetails_ca_alter_patientdetails_chol_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdetails',
            name='oldpeak',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
