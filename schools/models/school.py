import os
import uuid

from django.db import models
from datetime import date, datetime
from django.db.models import Q, Prefetch
from django.urls import reverse

class SchoolManager(models.Manager):

    def get_school_academic_session(self, school):
        from . import AcademicSession
        filters = Q(school=school) | (Q(school_type=school.school_type) | Q(school_type='all'))
        if '+' in school.program:
            programs = school.program.split('+')
            filters &= Q(program__in=programs)
        else:
            filters &= Q(program=school.program)

        return AcademicSession.objects.filter(filters, status='ongoing').first()

    def get_school_status(self, school):

        
        try:
            accr = school.recent_accreditation_status() 
        except (AttributeError, TypeError): 
            accr = None

        try:
            sus = school.get_latest_suspension_or_closure_report() 
        except (AttributeError, TypeError):
            sus = None

        if accr and accr.status == 'accreditated':
            if not sus:
                return 'Active'
        elif accr and accr.status == 'awaiting accreditation':
            if sus:
                return f"{sus.suspension_type} & {accr.status}"
            return accr.status

        if accr:
            return accr.status
        if sus:
            return sus.suspension_type
        return '-' 

    def get_levels_and_classes(self, school):
        """
        Fetch level classes and program levels for this school.
        """
        from schools.models import ProgramLevelTemplate, Stream, LevelClasses
        program_components = school.program.split('+') 

        # Query program levels for this school
        if program_components != 'all':
            program_levels = ProgramLevelTemplate.objects.filter(
                Q(program__in=program_components)
            ) 
        else:
            program_levels = ProgramLevelTemplate.objects.all()

        # Fetch level classes directly linked to this school
        classes = school.classes.prefetch_related('program_level_template', 'stream').all()
        unassociated_levels = program_levels.exclude(level_classes__school=school)
        return {'classes': classes, 'program_levels': unassociated_levels}

    def get_current_accreditation(self, school):
        # Get the current date
        today = date.today()
        
        # Retrieve the most recent accreditation status
        accr = school.recent_accreditation_status()
        
        # Ensure that the accreditation status exists
        if accr:
            # Check if the accreditation has expired
            if accr.valid_to and accr.valid_to < today:
                accr.expired = True
            
            # Return the accreditation if both 'valid_from' and 'valid_to' are available
            if accr.valid_from and accr.valid_to:
                return accr
        
        # Return None if accreditation is invalid or missing required dates
        return accr if accr else None 

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
    name = models.CharField(max_length=255, unique=True,  db_index=True)
    abbreviation = models.CharField(max_length=20, null=True, blank=True)
    motto = models.CharField(max_length=255, unique=True, blank=True, null=True)
    established_date = models.DateField(null=True, blank=True)

    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPE_CHOICES, default='public', db_index=True)
    is_vocational = models.BooleanField(default=False)
    program = models.CharField(max_length=12, choices=PROGRAM_CHOICES, default='all', db_index=True)
    logo = models.ImageField(upload_to='schools_logo/%Y/%m/%d/', blank=True, null=True)
 
    registration_number = models.CharField(max_length=50, unique=True, blank=True, null=True, db_index=True)

    # School Location Information
    lga = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=50, null=True, blank=True)  # Optional city field
    ward = models.CharField(max_length=50, default='')
    street_address = models.TextField(default='')

    # Contact Information
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=255, null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    # Geolocation Information
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,)
    

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        """
        Override save to handle file cleanup for the logo.
        """
        if not self.registration_number:
            self.registration_number = self.generate_registration_number()

        if self.pk and self.logo:
            try:
                old_logo = School.objects.get(pk=self.pk).logo
            except School.DoesNotExist:
                old_logo = None
            
            if old_logo and self.logo != old_logo:
                from schools.utils import remove_old_file
                if not remove_old_file(old_logo.path):
                    # Handle the case where file removal failed
                    import logging
                    logger.warning("Failed to remove old logo file.")  
        
        super().save(*args, **kwargs)

    def generate_registration_number(self):
        """
        Generate a unique registration number based on the school type using UUID.
        """
        school_type_code = {'public': '1', 'private': '2', 'community': '3'}
        type_code = school_type_code[self.school_type]
        unique_id = str(uuid.uuid4().int)[:7]
        return f"{type_code}{unique_id}"

    def __str__(self):
        return self.name
    
    def recent_accreditation_status(self):
        from . import AccreditationStatus

        accr = self.accreditationstatus_set.order_by("-created_at").first()
        return accr if accr else None 

    def get_latest_inspection_report(self):
        return self.inspectionreport_set.order_by("-date_created").first()

    def get_latest_suspension_or_closure_report(self):
        return self.suspensionclosure_set.order_by('-created_at').filter(is_dropped=False).first()

    objects = SchoolManager()

    def get_academic_session(self):
        return self.__class__.objects.get_school_academic_session(self)

    @property
    def status(self):
        return self.__class__.objects.get_school_status(self)

    def get_levels_and_classes(self):
        return self.__class__.objects.get_levels_and_classes(self)

    def get_current_accreditation(self):
        return self.__class__.objects.get_current_accreditation(self)

    def get_absolute_url(self):
        return reverse('schools:details', kwargs={'pk': self.pk})       
