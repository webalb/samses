# Generated by Django 5.0.6 on 2024-12-26 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0010_departmentrepository_schooldepartment_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='stream',
            index=models.Index(fields=['name'], name='schools_str_name_23a437_idx'),
        ),
        migrations.AddIndex(
            model_name='stream',
            index=models.Index(fields=['id'], name='schools_str_id_a74626_idx'),
        ),
    ]