from django.db import models

from .school import School

class Subject(models.Model):
    PROGRAM_CHOICES = [
        ('primary', 'Primary'),
        ('jss', 'Junior Secondary School'),
        ('sss', 'Senior Secondary School'),
        # ('primary+jss', 'Primary + Junior Secondary School'),
        # ('jss+sss', 'Junior Secondary School + Senior Secondary School'),
        # ('all', 'All Programs'),
    ]

    subject_name = models.CharField(max_length=50, blank=False)
    program = models.CharField(max_length=12, choices=PROGRAM_CHOICES, default='primary')
    is_general = models.BooleanField(default=True)
    is_optional = models.BooleanField(default=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='subjects', null=True, blank=True)

    def __str__(self):
        return self.subject_name

    def clean(self):
        # Ensure that general subjects cannot have a specific school assigned
        if self.is_general and self.school is not None:
            raise ValidationError("General subjects cannot be assigned to a specific school.")
        
        # Ensure that subjects for all programs have no specific school
        if self.is_optional and self.school is not None:
            raise ValidationError(f"Subjects marked optional should have a specific school assigned.")


    class Meta:
        unique_together = (
            ('subject_name', 'program', 'is_general',), # unique subject_name, program, and general
            ('subject_name', 'program', 'is_general', 'is_optional', 'school',), # for individual school, should has unique subject to same program either general or optional
        )
