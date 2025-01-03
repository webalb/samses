# Generated by Django 5.0.6 on 2024-12-26 16:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0009_alter_schoolsubject_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentRepository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('certification_awarded', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departments', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.departmentrepository')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_departments', to='schools.school')),
            ],
        ),
        migrations.DeleteModel(
            name='VocationalDepartment',
        ),
    ]
