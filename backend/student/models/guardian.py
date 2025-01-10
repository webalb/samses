from django.db import models
from django.core.validators import (
    RegexValidator,
)

from .student import Student

class Guardian(models.Model):
    RELATIONSHIP_CHOICES = [
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Guardian', 'Guardian'),
        ('Grandfather', 'Grandfather'),
        ('Grandmother', 'Grandmother'),
        ('Uncle', 'Uncle'),
        ('Aunt', 'Aunt'),
        ('Brother', 'Brother'),
        ('Sister', 'Sister'),
        ('Other', 'Other'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="guardians",
        help_text="The student this guardian is associated with.",
    )
    full_name = models.CharField(max_length=100, help_text="Guardian's full name.")
    relationship = models.CharField(
        max_length=50,
        choices=RELATIONSHIP_CHOICES,
        default='Father',
        help_text="Relationship to the student (e.g., Father, Mother, Uncle).",
    )
    role = models.CharField(max_length=1, choices=[
            ('1', 'Primary Guardian'),
            ('2', 'Financial Sponsor'),
            ('3', 'Emergency Contact'),
            # Add more choices as needed
        ], default='1')
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^(?:\+234|0)?[789]\d{9}$',
            message="Please use a valid Nigeria phone number"
            )],
        help_text="Guardian's phone number.",
    )
    email = models.EmailField(blank=True, null=True, help_text="Guardian's email address (optional).")
    address = models.TextField(blank=True, null=True, help_text="Guardian's address.")

    def __str__(self):
        return f"{self.full_name} ({self.relationship} of {self.student.full_name})"
