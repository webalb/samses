# Generated by Django 5.0.6 on 2024-12-27 15:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("schools", "0014_alter_schoolfeedback_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="gradeboundary",
            options={"ordering": ["grade"]},
        ),
        migrations.AddField(
            model_name="subjectrepository",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="subjectrepository",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
