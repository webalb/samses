import os
import uuid
from enum import unique
from typing import Required

from django.db import models
from datetime import date, datetime
from django.db.models import Q
from django.urls import reverse

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
    # School Identity Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default='')
    abbreviation = models.CharField(max_length=20, null=True, blank=True)
    motto = models.CharField(max_length=255, unique=True, blank=True, null=True)
    established_date = models.DateField(null=True, blank=True)
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPE_CHOICES, default='public')
    program = models.CharField(max_length=12, choices=PROGRAM_CHOICES, default='all')
    logo = models.ImageField(upload_to='schools_logo/%Y/%m/%d/', blank=True, null=True)
    
    registration_number = models.CharField(max_length=50, unique=True, default='', blank=True, null=True)

    # School Location Information
    lga = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=50, null=True, blank=True)  # Optional city field
    ward = models.CharField(max_length=50, default='')
    street_address = models.TextField(default='')

    # Contact Information
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    # Geolocation Information
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    

    def save(self, *args, **kwargs):

        if not self.registration_number:
            self.registration_number = self.generate_registration_number()

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
                        self.logo.name = f"{self.registration_number}_{self.logo.name}"
                # if logo is not change
                elif orig.logo and self.logo and orig.logo.name == self.logo.name:
                        self.logo.name = self.logo.name


        elif not self.logo.name:  # Ensure name is set if creating a new instance
            self.logo.name = f"{self.registration_number}_{self.logo.name}"

        super(School, self).save(*args, **kwargs)

    # generating school_number based on T-SSS algorithm as stated in BD Document
    def generate_registration_number(self):
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
            last_id = int(last_school.registration_number[4:])  # type: ignore # Get the numeric part of the last school ID
            unique_code = str(last_id + 1).zfill(3)
        return f"MOE{type_code}{unique_code}"

    def get_subjects(self):
        from . import Subject
        
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
        from . import AcademicSession

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

    def get_current_accreditation(self):
        from datetime import date
        # Get the current date
        today = date.today()
        
        # Retrieve the most recent accreditation status
        accr = self.recent_accreditation_status()
        
        # Ensure that the accreditation status exists
        if accr:
            # Check if the accreditation has expired
            if accr.valid_to and accr.valid_to < today:
                accr.expired = True
            
            # Return the accreditation if both 'valid_from' and 'valid_to' are available
            if accr.valid_from and accr.valid_to:
                return accr
        
        # Return None if accreditation is invalid or missing required dates
        return None

    def recent_accreditation_status(self):
        from . import AccreditationStatus

        accr = self.accreditationstatus_set.order_by("-created_at").first()
        return accr if accr else None 

    def get_latest_inspection_report(self):
        return self.inspectionreport_set.order_by("-date_created").first()

    def get_latest_suspension_or_closure_report(self):
        return self.suspensionclosure_set.order_by('-date_created').filter(is_dropped=False).first()

    @property
    def status(self):
        accr = self.recent_accreditation_status()
        if accr and accr.status == 'accreditated':
            if not self.get_latest_suspension_or_closure_report():
                return 'Active'
            return self.get_latest_suspension_or_closure_report().suspension_type
        return 'Under Investigation' 

    def get_absolute_url(self):
        return reverse('schools:details', kwargs={'pk': self.pk})       
