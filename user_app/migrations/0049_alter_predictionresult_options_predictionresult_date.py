# Generated by Django 4.2.5 on 2023-11-08 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0048_alter_predictionresult_patient'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='predictionresult',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='predictionresult',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
