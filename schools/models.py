from enum import unique
from django.db import models
from datetime import date
from django.db.models import Q
from django.core.exceptions import ValidationError

class School(models.Model):
    SCHOOL_TYPE_CHOICES = [
        ('public', 'Public School'),
        ('private', 'Private School'),
        ('community', 'Community School'),
    ]

    PROGRAM_CHOICES = [
        ('primary', 'Primary'),
        ('jss', 'Junior Secondary School'),
        ('all', 'All Programs'),
    ]

    school_number = models.CharField(max_length=4, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    moto = models.TextField(blank=True, null=True)
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPE_CHOICES, default='public')
    lga = models.CharField(max_length=50)
    ward = models.CharField(max_length=50)
    school_email = models.EmailField(max_length=255)
    school_phone_number = models.CharField(max_length=15)
    school_website = models.URLField(max_length=255, blank=True, null=True)
    program = models.CharField(max_length=10, choices=PROGRAM_CHOICES, default='all')
    logo = models.ImageField(upload_to='schools_logo/%Y/%m/%d/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.school_number:
            self.school_number = self.generate_school_number()
        if self.logo:
            self.logo.name = f"{self.school_number}_{self.logo.name}"
        super().save(*args, **kwargs)

    # generating school_number based on T-SSS algorithm as stated in BD Document
    def generate_school_number(self):
        school_type_code = {
            'public': '1',
            'private': '2',
            'community': '3',
        }
        type_code = school_type_code[self.school_type]
        last_school = School.objects.filter(school_type=self.school_type).order_by('id').last()
        if not last_school:
            unique_code = '001'
        else:
            last_id = int(last_school.school_number[1:])  # type: ignore # Get the numeric part of the last school ID
            unique_code = str(last_id + 1).zfill(3)
        return f"{type_code}{unique_code}"

    def __str__(self):
        return self.name
    
    def get_academic_session(self):
        from .models import AcademicSession

        individual_session = AcademicSession.objects.filter(
            school_type='individual',
            school=self
        ).first()

        if individual_session:
            return individual_session

        group_session = AcademicSession.objects.filter(
            Q(school_type=self.school_type) |
            Q(school_type='all')
        ).first()

        if group_session:
            return group_session

        return None
    
class AcademicSession(models.Model):
    SCHOOL_TYPE_CHOICES = [
        ('all', 'All schools'),
        ('public', 'Public schools'),
        ('private', 'Private schools'),
        ('community', 'Community schools'),
        ('individual', 'Individual schools'),
    ]

    school_type = models.CharField(max_length=10, choices=SCHOOL_TYPE_CHOICES, default='all')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='academic_sessions', null=True, blank=True)
    session_name = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        if self.school_type == 'all':
            return f"Session {self.session_name} set for: All schools"
        elif self.school_type == 'public':
            return f"Session {self.session_name} set for: All public schools"
        elif self.school_type == 'private':
            return f"Session {self.session_name} set for: All private schools"
        elif self.school_type == 'community':
            return f"Session {self.session_name} set for: All community schools"
        elif self.school_type == 'individual':
            return f"Session {self.session_name} set for: {self.school.name}" # type: ignore
    
    class Meta:
        unique_together = ('school', 'session_name')

    def duration(self):
        return (self.end_date - self.start_date).days

    def is_active(self):
        today = date.today()
        return self.start_date <= today <= self.end_date
    
    def on_coming(self):
        today = date.today()
        return today < self.start_date

    def get_academic_terms(self):
        from .models import Term

        individual_term = Term.objects.filter(
            school_type='individual',
            school=self
        )

        if individual_term:
            return individual_term

        group_term = Term.objects.filter(
            Q(school_type=self.school_type) |
            Q(school_type='all')
        )

        if group_term:
            return group_term

        return None

class Term(models.Model):
    TERMS = [
        ('1', 'First Term'),
        ('2', 'Second Term'),
        ('3', 'Third Term'),
    ]
    
    class Meta:
        unique_together = ('academic_session', 'term_name')

    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='terms')
    term_name = models.CharField(max_length=1, choices=TERMS, default='1')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.get_term_name_display()} - {self.academic_session.session_name}" # type: ignore

class Subject(models.Model):
    PROGRAM_CHOICES = [
        ('0', 'All Programs'),
        ('1', 'Primary'),
        ('2', 'Junior Secondary School'),
    ]

    subject_name = models.CharField(max_length=255)
    program = models.CharField(max_length=1, choices=PROGRAM_CHOICES, default='0')
    is_general = models.BooleanField(default=True)  # Indicates if the subject is general
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='subjects', null=True, blank=True)

    def __str__(self):
        return self.subject_name

    def save(self, *args, **kwargs):
        if self.is_general:
            self.school = None  # General subjects should not be linked to a specific school
        super().save(*args, **kwargs)
