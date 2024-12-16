from django.db import models

from schools.models import School

class SchoolRelatedModel(models.Model):
    """
    Abstract base class for models that need a school field.
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="%(class)s")
    images_description = models.TextField(blank=True, null=True, help_text="Optional description of the image.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Classrooms(SchoolRelatedModel):
    """
    Stores details about classrooms.
    """
    number_of_classrooms = models.PositiveSmallIntegerField(default=0)
    classrooms_availability = models.TextField(blank=True)

    def __str__(self):
        return f"Classrooms for {self.school.name}"


class Library(SchoolRelatedModel):
    """
    Stores library details.
    """
    book_count = models.PositiveIntegerField(default=0)
    digital_access = models.BooleanField(default=False)
    study_space_capacity = models.PositiveIntegerField(blank=True, null=True)
    library_availability = models.TextField(blank=True)

    def __str__(self):
        return f"Library for {self.school.name}"


class Laboratory(SchoolRelatedModel):
    """
    Stores laboratory details.
    """
    lab_type = models.CharField(max_length=100, choices=[
        ('Physics Lab', 'Physics Lab'),
        ('Chemistry Lab', 'Chemistry Lab'),
        ('Biology Lab', 'Biology Lab'),
        ('Robotics Lab', 'Robotics Lab'),
    ])
    lab_equipment = models.TextField(blank=True)
    lab_availability = models.TextField(blank=True)

    def __str__(self):
        return f"{self.lab_type} for {self.school.name}"


class ComputerLab(SchoolRelatedModel):
    """
    Stores details about computer labs.
    """
    number_of_computers = models.PositiveIntegerField(default=0)
    internet_access = models.BooleanField(default=False)
    smart_classrooms = models.BooleanField(default=False)
    computer_lab_availability = models.TextField(blank=True)

    def __str__(self):
        return f"Computer Lab for {self.school.name}"


class SportsFacility(SchoolRelatedModel):
    """
    Stores details about sports facilities.
    """
    facility_type = models.CharField(max_length=100, choices=[
        ('Football Field', 'Football Field'),
        ('Basketball Court', 'Basketball Court'),
        ('Volleyball Court', 'Volleyball Court'),
        ('Swimming Pool', 'Swimming Pool'),
    ])
    field_availability = models.TextField(blank=True)

    def __str__(self):
        return f"Sports Facility for {self.school.name}"


class SchoolImages(SchoolRelatedModel):
    """
    Stores images for various infrastructure types.
    """
    images_description = None
    image_type = models.CharField(max_length=50,)
    image = models.ImageField(upload_to='infrastructure_images/%Y/%m/%d/')

    def __str__(self):
        return f"{self.image_type.capitalize()} Image for {self.school.name}"
