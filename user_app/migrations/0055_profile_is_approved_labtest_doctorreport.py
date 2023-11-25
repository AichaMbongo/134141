# Generated by Django 4.2.5 on 2023-11-25 10:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_app', '0054_alter_patientvitals_blood_pressure'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_approved',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='LabTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_type', models.CharField(max_length=255)),
                ('test_date', models.DateField(auto_now_add=True)),
                ('patient_name', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('awaiting', 'Awaiting Test'), ('completed', 'Test Completed')], default='awaiting', max_length=20)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.patient')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_date', models.DateField(auto_now_add=True)),
                ('symptoms', models.TextField()),
                ('diagnosis', models.TextField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.patient')),
            ],
        ),
    ]
