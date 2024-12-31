from django.db import models
from django.core.exceptions import ValidationError

from schools.models import School

class ProgramLevelTemplate(models.Model):
    SCHOOL_PROGRAM_CHOICES = [
        ('primary', 'Primary'),
        ('jss', 'Junior Secondary School'),
        ('sss', 'Senior Secondary School'),
    ]

    program = models.CharField(max_length=7, choices=SCHOOL_PROGRAM_CHOICES)
    level = models.CharField(max_length=9, help_text="Level name (e.g., Primary 1, JSS 2).")

    class Meta:
        unique_together = ('program', 'level')

    def __str__(self):
        return f"{self.get_program_display()} - {self.level}"

# this also is a fixed data model there for create the fixture for it
class Stream(models.Model):
    STREAM_CHOICES = [
        ('science', 'Science'),
        ('arts', 'Arts'),
        ('commercial', 'Commercial'),
    ]

    program_level_template = models.ForeignKey(
        ProgramLevelTemplate,
        on_delete=models.CASCADE,
        related_name="streams",
        help_text="The level this stream belongs to (e.g., SSS 1, JSS 2)."
    )
    name = models.CharField(max_length=10, choices=STREAM_CHOICES)

    def __str__(self):
        return f"{self.get_name_display()} - {self.program_level_template.level}"

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['id']),
        ]

    @classmethod
    def get_queryset(cls):
        return super().get_queryset().order_by('name').distinct('name') 

class LevelClasses(models.Model):
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name='classes')
    program_level_template = models.ForeignKey(ProgramLevelTemplate, on_delete=models.CASCADE, related_name="level_classes")
    class_section_name = models.CharField(max_length=50, help_text="Name of the section (e.g., A, B, Usman Ibn Affan).")
    stream = models.ForeignKey(Stream, null=True, blank=True, on_delete=models.CASCADE, related_name="class_sections")
    capacity = models.PositiveIntegerField(default=0, blank=True, null=True, help_text="Number of students this class can accommodate.")


    def clean(self):
        """
        Custom validation to ensure no duplicate class_section_name exists
        for the same program_level_template.
        """    
        # Ensure that streams only apply to SSS levels
        if self.stream:
            self.program_level_template = self.stream.program_level_template
        if self.stream and self.program_level_template.program != 'sss':
            raise ValidationError("Streams are only applicable to Senior Secondary School levels.")
        

    def save(self, *args, **kwargs):
        # Trigger validation before saving

        self.full_clean()
        super().save(*args, **kwargs) 
    def __str__(self):
        return f"Section {self.class_section_name} ({self.program_level_template.level})"

    class Meta:
        unique_together = ('program_level_template', 'class_section_name', 'school')

