# Generated by Django 4.2.5 on 2023-10-22 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0032_alter_treatmentplan_patient'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='treatmentplan',
            options={'ordering': ['-id']},
        ),
    ]
