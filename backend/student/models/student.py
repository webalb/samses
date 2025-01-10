import os
import re
import uuid
from django.db import models
from django.urls import reverse

from django.core.exceptions import ValidationError
from django.core.validators import (
    EmailValidator,
    RegexValidator,
    MinLengthValidator,
    FileExtensionValidator,
)
from datetime import date

from backend.schools.models import School

# Custom validator for text fields
def alphabet_space_hyphen_validator(value):
    if not re.match(r'^[a-zA-Z\s-]+$', value):
        raise ValidationError('This field can only contain alphabets, spaces, and hyphens.')

def validate_image(image):
    # Check file size
    max_size = 1 * 1024 * 1024  # 1 MB
    if image.size > max_size:
        raise ValidationError(f"Image file too large ( > {max_size} bytes )")
    return image

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), 
        ('B+', 'B+'), ('B-', 'B-'), 
        ('AB+', 'AB+'), ('AB-', 'AB-'), 
        ('O+', 'O+'), ('O-', 'O-')
    ]

    GENOTYPE_CHOICES = [
        ('AA', 'AA'),
        ('AS', 'AS'),
        ('SS', 'SS'),
        ('SC', 'SC'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(
        max_length=25,
        validators=[MinLengthValidator(2), alphabet_space_hyphen_validator]
    )
    last_name = models.CharField(
        max_length=25,
        validators=[MinLengthValidator(2), alphabet_space_hyphen_validator]
    )
    middle_name = models.CharField(
        max_length=25,
        blank=True,
        validators=[alphabet_space_hyphen_validator]
    )
    nin_number = models.CharField( 
            max_length=12,
            blank=True, 
            null=True, 
            validators=[
                RegexValidator(r'^[1-9]\d{0,10}$', 
                message='Only positive integers allowed.'
            )],
            help_text="Student's NIN Number (optional)."
        )

    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    blood_group = models.CharField(
        max_length=3, 
        choices=BLOOD_GROUP_CHOICES, 
        blank=True, 
        null=True, 
        help_text="Student's blood group."
    )
    genotype = models.CharField(
        max_length=2, 
        choices=GENOTYPE_CHOICES, 
        blank=True, 
        null=True, 
        help_text="Student's genotype."
    )
    disability_status = models.TextField(
        blank=True, 
        null=True, 
        help_text="Details about any disabilities the student has."
    )

    country_of_birth = models.CharField(
        max_length=25,
        validators=[MinLengthValidator(4), alphabet_space_hyphen_validator]
    )
    state_of_origin = models.CharField(
        max_length=25,
        validators=[MinLengthValidator(4), alphabet_space_hyphen_validator]
    )
    place_of_birth = models.CharField(
        max_length=25,
        validators=[MinLengthValidator(4), alphabet_space_hyphen_validator]
    )
    address = models.TextField(blank=True, null=True, help_text="Home address of the student.")

    passport_photograph = models.ImageField(
        upload_to='students/passport/%Y/%m/%d/',
        unique=True,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png']), validate_image]
    )

    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
        help_text="The school this student is registered to.",
    )

    reg_num = models.CharField(max_length=11, unique=True)


    # Metadata
    is_active = models.BooleanField(default=True, help_text="Indicates if the student is currently active.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Record creation timestamp.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Record last updated timestamp.")

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['last_name', 'first_name']
        unique_together = (('first_name', 'last_name', 'date_of_birth', 'state_of_origin', 'place_of_birth'),)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('student:details', args=[str(self.pk)])

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()
    
    @property
    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age

    def generate_unique_reg_num(self):
        while True:
            reg_num = str(uuid.uuid4().int)[:11]  # Get first 11 characters of UUID
            if not Student.objects.filter(reg_num=reg_num).exists():
                return reg_num

    def clean(self):
        """
        Validates the date of birth.
        Raises a ValidationError if the date of birth is less than 4 years before today's date.
        """
        super().clean() 

        dob = self.date_of_birth
        if not dob:
            return  # No need to validate if dob is not provided

        today = date.today()
        min_allowed_dob = today.replace(year=today.year - 4)
        if dob > min_allowed_dob:
            raise ValidationError("Student must be at least 4 years old.")

    def save(self, *args, **kwargs):
        # Check if a new passport_photograph file is uploaded and update its name
        if not self.reg_num:
            self.reg_num = self.generate_unique_reg_num()

        if self.pk and self.passport_photograph:
            try:
                old_passport_photograph = Student.objects.get(pk=self.pk).passport_photograph
            except Student.DoesNotExist:
                old_passport_photograph = None
            
            if old_passport_photograph and self.passport_photograph != old_passport_photograph:
                from backend.schools.utils import remove_old_file
                if not remove_old_file(old_passport_photograph.path):
                    # Handle the case where file removal failed
                    import logging
                    logger.warning("Failed to remove old passport photograph file.")  

        super().save(*args, **kwargs)
