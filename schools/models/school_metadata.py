from django.db import models
from .school import School

# School Academic Information
class SchoolMetadata(models.Model):
    """Metadata settings for school-related information."""
    
    LANGUAGES = [
        ("en", "English"),
        ("hs", "Hausa"),
        ("ff", "Fulfulde"),
        ("yb", "Yoruba"),
        ("ig", "Igbo"),
    ]
    
    OWNERSHIP_OPTIONS = [
        ('state government', 'State Government'),
        ('local government', 'Local Government'),
        ('private individual', 'Private Individual'),
        ('religious body', 'Religious Body'),
        ('community', 'Community'),
    ]
    
    school = models.OneToOneField(School, on_delete=models.CASCADE)
    
    language_of_instruction = models.CharField(
        max_length=2, 
        choices=LANGUAGES, 
        default=LANGUAGES[0][0], 
        help_text="Primary language(s) used in teaching"
    )
    
    enrollment_capacity = models.PositiveSmallIntegerField(
        blank=True, 
        null=False, 
        help_text="Annual enrollment capacity of the school."
    )
    
    ownership_status = models.CharField(
        max_length=30, 
        choices=OWNERSHIP_OPTIONS, 
  		default='state government',  # Set default value as string, not a tuple
        help_text="Ownership status of the school")    
    owner = models.CharField(
        max_length=110, 
        default='', 
        help_text="Name of the owner, e.g., JIBWIS JOS, Akko Local Government", 
        blank=True, 
        null=False
    )

    # Fields for school’s performance metrics
    pass_rate = models.DecimalField(
        max_digits=5, decimal_places=2, 
        null=True, blank=True, 
        help_text="Pass rate as a percentage of students passing exams"
    )
    
    graduation_rate = models.DecimalField(
        max_digits=5, decimal_places=2, 
        null=True, blank=True, 
        help_text="Percentage of students graduating each year"
    )
    
    attendance_rate = models.DecimalField(
        max_digits=5, decimal_places=2, 
        null=True, blank=True, 
        help_text="Student attendance rate as a percentage"
    )
    
    discipline_rate = models.DecimalField(
        max_digits=5, decimal_places=2, 
        null=True, blank=True, 
        help_text="Percentage of disciplinary incidents"
    )
    
    # Field for school's compliance standard
    compliance_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, 
        null=True, blank=True, 
        help_text="Record of the school's compliance with standards as a percentage (e.g., 80%)."
    )
    
    def __str__(self):
        return f"Metadata for {self.school.name}"

