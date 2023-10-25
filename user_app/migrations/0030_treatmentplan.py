# Generated by Django 4.2.5 on 2023-10-22 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0029_alter_patientdetails_fbs'),
    ]

    operations = [
        migrations.CreateModel(
            name='TreatmentPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medications', models.TextField()),
                ('lifestyle_changes', models.TextField()),
                ('follow_up_date', models.DateField()),
                ('additional_notes', models.TextField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.patient')),
            ],
        ),
    ]
