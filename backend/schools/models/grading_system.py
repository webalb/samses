from django.db import models

from .school import School
from .subject import SubjectRepository
from .levels_and_classes import ProgramLevelTemplate

class GradingScale(models.Model):
    """
    Model for defining grading scales for a school.
    """
    
    scale_name = models.CharField(max_length=100, help_text="Name of the grading scale (e.g., Standard Scale).")
    description = models.TextField(blank=True, help_text="Description of the grading scale.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.scale_name}"

class GradeBoundary(models.Model):
    """
    Model for defining grade boundaries within a grading scale.
    """
    grading_scale = models.ForeignKey(
        'GradingScale',
        on_delete=models.CASCADE,
        related_name='grade_boundaries',
        help_text="The grading scale this boundary belongs to."
    )
    grade = models.CharField(max_length=2, help_text="Grade label (e.g., A, B, C).")
    lower_bound = models.PositiveSmallIntegerField(help_text="Minimum score for this grade.")
    upper_bound = models.PositiveSmallIntegerField(help_text="Maximum score for this grade.")
    description = models.TextField(blank=True, help_text="Additional details about this grade boundary.")

    class Meta:
        unique_together = ('grading_scale', 'grade')
        ordering = ['grade']

    def __str__(self):
        return f"{self.grade}: {self.lower_bound}-{self.upper_bound} ({self.grading_scale.scale_name})"

class SubjectGradingConfiguration(models.Model):
    
    """
    Model for customizing grading configuration for specific subjects or levels.
    """
    
    subject = models.ForeignKey(
        'SubjectRepository',
        on_delete=models.CASCADE,
        related_name='grading_configurations',
        help_text="The subject this grading configuration applies to."
    )
    grading_scale = models.ForeignKey(
        'GradingScale',
        on_delete=models.CASCADE,
        related_name='subject_configs',
        help_text="The grading scale to be used for this subject."
    )
    
    """
    The weightage field in this model represents the
    relative importance of a subject in the overall grade calculation.
    It allows schools to assign different levels of significance to various
    subjects when determining a student's total grade or performance.
    """
    weightage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100.00,
        help_text="Weightage of the subject in the total grade calculation."
    )

    def __str__(self):
        return f"{self.subject.subject_name} ({self.grading_scale.scale_name})"
