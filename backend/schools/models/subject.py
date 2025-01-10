from django.db import models
from django.core.exceptions import ValidationError
from .school import School 

from .levels_and_classes import ProgramLevelTemplate, Stream
from .vocational_schools import DepartmentRepository

"""
Modified Subject Management Architecture

- Ministry-Managed Subjects:
    - The Ministry of Education manages a central repository of all subjects.
    - Each subject is defined with:
        - Name: Unique identifier for the subject (e.g., Mathematics, Physics).
        - Category: Core, Religious, Vocational, or Local Language.
        - Program Levels: Primary, JSS, SSS, or combinations.
        - Streams: Applicable streams (e.g., Science, Arts).
    - This eliminates duplication of subjects across schools in the database.

- School-Specific Subject Offerings:
    - Schools do not create subjects directly.
    - Instead, schools select subjects from the central repository based on their curriculum requirements and available resources.
    - Selection is tied to the school's program levels and streams. 
        - For example, a school offering SSS Science selects Physics and Chemistry for the Science stream.

- Student Registration and Subject Assignment:
    - During student registration, subjects are assigned dynamically based on:
        - The student's program level and stream.
        - Selective options (e.g., Religious subjects based on the student's religion).
    - The system ensures that only subjects offered by the school at the student's level are displayed.
"""

from django.core.exceptions import ValidationError
from django.db import models

class SubjectRepository(models.Model):
    SUBJECT_CATEGORY_CHOICES = [
        ('core', 'Core'),
        ('religious', 'Religious'),
        ('vocational', 'Vocational'),
        ('local_language', 'Local Language'),
    ]

    subject_name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SUBJECT_CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    program_levels = models.ManyToManyField(ProgramLevelTemplate, related_name="repository_subjects")
    streams = models.ManyToManyField(Stream, blank=True, related_name="repository_subjects")

    vocational_department = models.ForeignKey(
        DepartmentRepository,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subjects",
        help_text="Applicable only for vocational subjects."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        # Fetch the associated program names
        programs = ", ".join(
            {level.get_program_display() for level in self.program_levels.all()}
        )
        if self.vocational_department:
            return f"{self.subject_name} ({self.get_category_display()} department: {self.vocational_department }) - Programs: {programs if programs else 'None'}"
        return f"{self.subject_name} ({self.get_category_display()}) - Programs: {programs if programs else 'None'}"


    def clean(self):
        super().clean()
        # Ensure vocational subjects have a vocational department
        if self.category == 'vocational' and not self.vocational_department:
            raise ValidationError("Vocational subjects must be linked to a vocational department.")
        # Ensure non-vocational subjects do not have a vocational department
        if self.category != 'vocational' and self.vocational_department:
            raise ValidationError("Non-vocational subjects cannot be linked to a vocational department.")


class SchoolSubject(models.Model):
    """
    Represents the subjects offered by a school.
    """
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="offered_subjects",
        help_text="The school offering this subject."
    )
    subject_repository = models.ForeignKey(
        SubjectRepository,
        on_delete=models.CASCADE,
        related_name="school_subjects",
        help_text="The subject from the central repository."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates if this subject is currently active/offered by the school."
    )
    is_compulsory = models.BooleanField(
        default=True,
        help_text="Indicates if this subject is compulsory for students at the school."
    )

    class Meta:
        unique_together = ('school', 'subject_repository')
        verbose_name = "School Subject"
        verbose_name_plural = "School Subjects"

    def __str__(self):
        status = "Compulsory" if self.is_compulsory else "Optional"
        return f"{self.subject_repository.subject_name} ({self.school.name}) - {status}"
