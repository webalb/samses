# Generated by Django 5.0.6 on 2024-12-27 11:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0013_subjectrepository_vocational_department'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schoolfeedback',
            options={'ordering': ['-created_at'], 'verbose_name': 'School Feedback', 'verbose_name_plural': 'School Feedbacks'},
        ),
        migrations.RemoveField(
            model_name='gradingscale',
            name='school',
        ),
        migrations.AddField(
            model_name='subjectgradingconfiguration',
            name='grading_scale',
            field=models.ForeignKey(default='', help_text='The grading scale to be used for this subject.', on_delete=django.db.models.deletion.CASCADE, related_name='subject_configs', to='schools.gradingscale'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subjectgradingconfiguration',
            name='subject',
            field=models.ForeignKey(default='', help_text='The subject this grading configuration applies to.', on_delete=django.db.models.deletion.CASCADE, related_name='grading_configurations', to='schools.subjectrepository'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subjectgradingconfiguration',
            name='weightage',
            field=models.DecimalField(decimal_places=2, default=100.0, help_text='Weightage of the subject in the total grade calculation.', max_digits=5),
        ),
    ]