# Generated by Django 5.0.6 on 2024-12-23 13:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0004_remove_programlevel_school_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='levelclasses',
            name='school',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='schools.school'),
            preserve_default=False,
        ),
    ]