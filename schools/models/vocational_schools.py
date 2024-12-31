# Specific models for vocational schools
from django.db import models

from schools.models import School

class DepartmentRepository(models.Model):
    department = models.CharField(max_length=100, help_text='Name of the department')
    description = models.TextField(blank=True)
    certification_awarded = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return self.department

class SchoolDepartment(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school_departments')
    departments = models.ForeignKey(DepartmentRepository, on_delete=models.CASCADE,)

    def __str__(self):
        return f"{self.school.name} - {self.departments.department}"


class VocationalPartnership(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="vocational_partnerships")
    partner_name = models.CharField(max_length=100)
    partnership_type = models.CharField(
        max_length=50,
        choices=[
            ("Industry", "Industry"),
            ("Government", "Government"),
            ("NGO", "NGO"),
        ],
    )
    description = models.TextField(blank=True, help_text="Details of the partnership.")
    partner_address = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.partner_name} ({self.school.name})"
