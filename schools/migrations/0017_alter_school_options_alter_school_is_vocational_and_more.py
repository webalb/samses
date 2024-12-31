# Generated by Django 5.0.6 on 2024-12-29 10:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("schools", "0016_remove_specialneedsresource_id_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="school",
            options={"ordering": ["name"]},
        ),
        migrations.AlterField(
            model_name="school",
            name="is_vocational",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="school",
            name="name",
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="school",
            name="registration_number",
            field=models.CharField(
                blank=True, db_index=True, max_length=50, null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="school",
            name="school_type",
            field=models.CharField(
                choices=[
                    ("public", "Public School"),
                    ("private", "Private School"),
                    ("community", "Community School"),
                ],
                db_index=True,
                default="public",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="staff",
            name="school",
            field=models.ForeignKey(
                help_text="The school this staff member belongs to.",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="staffs",
                to="schools.school",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="feestructure",
            unique_together={("class_level", "fee_type")},
        ),
    ]
