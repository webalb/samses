import os
import re
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import (
    EmailValidator,
    RegexValidator,
    MinLengthValidator,
    FileExtensionValidator,
)
from datetime import date


from schools.models import School
from students.algorithms import generate_luhn_check_digit

# Custom validator for text fields
def alphabet_space_hyphen_validator(value):
    if not re.match(r'^[a-zA-Z\s-]+$', value):
        raise ValidationError('This field can only contain alphabets, spaces, and hyphens.')

def validate_image(image):
    # Check file size
    max_size = 1 * 1024 * 1024  # 5 MB
    if image.size > max_size:
        raise ValidationError(f"Image file too large ( > {max_size} bytes )")
    return image

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    LEVEL_CHOICES = [
        ('1', 'Primary 1'),
        ('2', 'Primary 2'),
        ('3', 'Primary 3'),
        ('4', 'Primary 4'),
        ('5', 'Primary 5'),
        ('6', 'Primary 6'),
        ('7', 'JSS 1'),
        ('8', 'JSS 2'),
        ('9', 'JSS 3'),
        ('10', 'SSS 1'),
        ('11', 'SSS 2'),
        ('12', 'SSS 3'),
    ]
    PROGRAM_CHOICES = [
        ('primary', 'Primary'),
        ('jss', 'Junior Secondary School'),
        ('sss', 'Senior Secondary School'),
    ]

    first_name = models.CharField(
        max_length=25,
        validators=[
            MinLengthValidator(2),
            alphabet_space_hyphen_validator
        ]
    )
    last_name = models.CharField(
        max_length=25,
        validators=[
            MinLengthValidator(2),
            alphabet_space_hyphen_validator
        ]
    )
    middle_name = models.CharField(
        max_length=25,
        blank=True,
        validators=[alphabet_space_hyphen_validator]
    )
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    country_of_birth = models.CharField(
        max_length=25,
        validators=[
            MinLengthValidator(2),
            alphabet_space_hyphen_validator
        ]
    )
    state_of_origin = models.CharField(
        max_length=25,
        validators=[
            MinLengthValidator(2),
            alphabet_space_hyphen_validator
        ]
    )
    place_of_birth = models.CharField(
        max_length=25,
        validators=[
            MinLengthValidator(2),
            alphabet_space_hyphen_validator
        ]
    )
    guardian_email = models.EmailField(
        blank=True,
        validators=[EmailValidator()]
    )
    guardian_phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    admission_number = models.CharField(
        max_length=8,
        unique=True,
        blank=True,
        editable=False
    )
    passport_photograph = models.ImageField(
        upload_to='students_passport/%Y/%m/%d/',
        unique=True,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png']),
            validate_image
            ]
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='students'
    )
    program = models.CharField(
        max_length=12,
        choices=PROGRAM_CHOICES,
        default='primary'
    )
    current_level = models.CharField(
        max_length=2,
        choices=LEVEL_CHOICES,
        default='1'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()

    def get_age(self):

        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age

    def save(self, *args, **kwargs):
        if not self.id:  # type: ignore # Only generate admission number if creating a new instance
            last_student = Student.objects.order_by('-admission_number').first()
            if last_student:
                last_number = int(last_student.admission_number[:-1])  # Strip the last digit
                new_number = last_number + 1
            else:
                new_number = 1

            admission_number_base = f"{new_number:07d}"  # Ensure 7 digits
            check_digit = generate_luhn_check_digit(admission_number_base)

            self.admission_number = f"{admission_number_base}{check_digit}"
                # Check if a new passport_photograph file is uploaded and update its name
        if self.passport_photograph:
            # Check if the instance already exists (i.e., updating an existing school)
            if self.pk:
                # Retrieve the original instance from the database
                orig = Student.objects.get(pk=self.pk)

                # Check if the passport_photograph field has changed
                if orig.passport_photograph and self.passport_photograph and orig.passport_photograph.name != self.passport_photograph.name:
                    # Delete the old passport_photograph file from the system
                    if os.path.isfile(orig.passport_photograph.path):
                        os.remove(orig.passport_photograph.path)
                        self.passport_photograph.name = f"{self.admission_number}_{self.passport_photograph.name.split('/')[-1]}"
                # if passport_photograph is not change
                elif orig.passport_photograph and self.passport_photograph and orig.passport_photograph.name == self.passport_photograph.name:
                        self.passport_photograph.name = self.passport_photograph.name


        elif not self.passport_photograph.name:  # Ensure name is set if creating a new instance
            self.passport_photograph.name = f"{self.admission_number}_{self.passport_photograph.name.split('/')[-1]}"

    
        super(Student, self).save(*args, **kwargs)

    def clean(self):
        # Custom validation to check for duplicate students
        if Student.objects.filter(
            first_name=self.first_name,
            last_name=self.last_name,
            date_of_birth=self.date_of_birth,
            guardian_phone_number=self.guardian_phone_number
        ).exclude(pk=self.pk).exists():
            raise ValidationError('A student with these details already exists.')


# next model