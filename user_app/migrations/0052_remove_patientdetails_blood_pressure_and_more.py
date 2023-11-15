# Generated by Django 4.2.5 on 2023-11-15 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0051_alter_profile_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientdetails',
            name='blood_pressure',
        ),
        migrations.RemoveField(
            model_name='patientdetails',
            name='heart_rate',
        ),
        migrations.RemoveField(
            model_name='patientdetails',
            name='respiratory_rate',
        ),
        migrations.RemoveField(
            model_name='patientdetails',
            name='temperature',
        ),
        migrations.CreateModel(
            name='PatientVitals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('blood_pressure', models.CharField(blank=True, max_length=10, null=True)),
                ('heart_rate', models.IntegerField(blank=True, null=True)),
                ('respiratory_rate', models.IntegerField(blank=True, null=True)),
                ('dateModified', models.DateTimeField(blank=True, null=True)),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user_app.patient')),
            ],
        ),
    ]