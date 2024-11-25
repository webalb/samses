# Generated by Django 5.0.6 on 2024-11-22 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0003_alter_school_registration_number_stakeholder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stakeholder',
            name='position',
            field=models.CharField(choices=[('Principal', 'Principal'), ('Director', 'Director'), ('Liaison Officer', 'Liaison Officer'), ('Board Member', 'Board Member'), ('Trustee', 'Trustee'), ('Academic Staff', 'Academic Staff'), ('Non Academic Staff', 'Non-Academic Staff')], max_length=50),
        ),
    ]
