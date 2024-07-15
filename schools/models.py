from enum import unique
from typing import Required
from django.db import models
from datetime import date
from django.db.models import Q
# from django.core.exceptions import ValidationError
import os

class School(models.Model):
    SCHOOL_TYPE_CHOICES = [
        ('public', 'Public School'),
        ('private', 'Private School'),
        ('community', 'Community School'),
    ]
    PROGRAM_CHOICES = [
        ('primary', 'Primary'),
        ('jss', 'Junior Secondary School'),
        ('sss', 'Senior Secondary School'),
        ('primary+jss', 'Primary + Junior Secondary School'),
        ('jss+sss', 'Junior Secondary School + Senior Secondary School'),
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
    program = models.CharField(max_length=12, choices=PROGRAM_CHOICES, default='all')
    logo = models.ImageField(upload_to='schools_logo/%Y/%m/%d/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.school_number:
            self.school_number = self.generate_school_number()

        # Check if a new logo file is uploaded and update its name
        if self.logo:
            # Check if the instance already exists (i.e., updating an existing school)
            if self.pk:
                # Retrieve the original instance from the database
                orig = School.objects.get(pk=self.pk)

                # Check if the logo field has changed
                if orig.logo and self.logo and orig.logo.name != self.logo.name:
                    # Delete the old logo file from the system
                    if os.path.isfile(orig.logo.path):
                        os.remove(orig.logo.path)
                        self.logo.name = f"{self.school_number}_{self.logo.name}"
                # if logo is not change
                elif orig.logo and self.logo and orig.logo.name == self.logo.name:
                        self.logo.name = self.logo.name


        elif not self.logo.name:  # Ensure name is set if creating a new instance
            self.logo.name = f"{self.school_number}_{self.logo.name}"

        super(School, self).save(*args, **kwargs)

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

    def get_subjects(self):
        from .models import Subject
        
        # Define a mapping for combined programs
        program_mapping = {
            'primary': ['primary'],
            'jss': ['jss'],
            'sss': ['sss'],
            'primary+jss': ['primary', 'jss'],
            'jss+sss': ['jss', 'sss'],
            'all': ['primary', 'jss', 'sss']
        }
        
        # Get the applicable programs for this school
        applicable_programs = program_mapping.get(self.program, [])
        
        # Query for subjects
        subjects = Subject.objects.filter(
            Q(program__in=applicable_programs),
            Q(school=self) | Q(school__isnull=True)
        ).order_by('program')
        
        return subjects

    def __str__(self):
        return self.name
    
    def get_academic_session(self):
        from .models import AcademicSession

        # Check for individual session matching school, school_type, and program
        individual_session = AcademicSession.objects.filter(
            school_type='individual',
            school=self,
            program=self.program
        ).first()

        if individual_session:
            return individual_session

        # Check for group session matching school type and program
        group_session = AcademicSession.objects.filter(
            Q(school_type=self.school_type) |
            Q(school_type='all'),
            program=self.program
        ).first()

        if group_session:
            return group_session

        # Handle combined programs like 'primary+jss', 'jss+sss'
        combined_programs = {
            'primary+jss': ['primary', 'jss'],
            'jss+sss': ['jss', 'sss']
            # Add more combinations as needed
        }

        # Check for sessions that match any of the programs in combined_programs
        for combined, programs in combined_programs.items():
            if self.program == combined:
                combined_session = AcademicSession.objects.filter(
                    Q(school_type=self.school_type) |
                    Q(school_type='all'),
                    program__in=programs
                ).first()

                if combined_session:
                    return combined_session

        return None
  
class AcademicSession(models.Model):
    SCHOOL_TYPE_CHOICES = [
        ('all', 'All schools'),
        ('public', 'Public schools'),
        ('private', 'Private schools'),
        ('community', 'Community schools'),
        ('individual', 'Individual schools'),
    ]
    PROGRAM_CHOICES = [
        ('primary', 'Primary Schools'),
        ('jss', 'Junior Secondary Schools'),
        ('sss', 'Senior Secondary Schools'),
        ('primary+jss', 'Primary + Junior Secondary Schools'),
        ('jss+sss', 'Junior Secondary Schools + Senior Secondary Schools'),
        ('all', 'All Programs'),
    ]
 
    school_type = models.CharField(max_length=10, choices=SCHOOL_TYPE_CHOICES, default='all')
    program = models.CharField(max_length=12, choices=PROGRAM_CHOICES, default='all')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='academic_sessions', null=True, blank=True)
    session_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        if self.school_type == 'all':
            return f"Session {self.session_name}, set for All schools, and for all {self.program}"
        elif self.school_type == 'public':
            return f"Session {self.session_name} set for: All public schools, and for all {self.program}"
        elif self.school_type == 'private':
            return f"Session {self.session_name} set for: All private schools, and for all {self.program}"
        elif self.school_type == 'community':
            return f"Session {self.session_name} set for: All community schools, and for all {self.program}"
        elif self.school_type == 'individual':
            return f"Session {self.session_name} set for: {self.school.name}, and for its {self.program}" # type: ignore

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

    def get_term(self):
        return Term.objects.filter(academic_session=self)

class Term(models.Model):
    academic_session = models.OneToOneField(AcademicSession, on_delete=models.CASCADE, related_name='term_dates')
    start_date_1 = models.DateField(null=True, blank=True)
    end_date_1 = models.DateField(null=True, blank=True)
    start_date_2 = models.DateField(null=True, blank=True)
    end_date_2 = models.DateField(null=True, blank=True)
    start_date_3 = models.DateField(null=True, blank=True)
    end_date_3 = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Terms for {self.academic_session.session_name}"

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