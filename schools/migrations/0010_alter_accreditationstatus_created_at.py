# Generated by Django 5.0.6 on 2024-11-25 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0009_alter_accreditationstatus_accreditation_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accreditationstatus',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]