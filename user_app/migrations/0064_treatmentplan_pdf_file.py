# Generated by Django 4.2.5 on 2023-11-30 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0063_alter_labtest_test_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='treatmentplan',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='pdf_files/'),
        ),
    ]