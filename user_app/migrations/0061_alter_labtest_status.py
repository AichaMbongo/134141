# Generated by Django 4.2.5 on 2023-11-26 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0060_doctorcomments_patient_alter_doctorcomments_doctor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labtest',
            name='status',
            field=models.CharField(choices=[('awaiting', 'Awaiting Test'), ('completed', 'Test Completed'), ('noNeed', 'No need for test')], default='noNeed', max_length=20),
        ),
    ]