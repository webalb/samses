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
