import os
from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_delete


from backend.schools.models import School

class SchoolRelatedModel(models.Model):
    """
    Abstract base class for models that need a school field.
    """
    school = models.OneToOneField(School, on_delete=models.CASCADE, primary_key=True)
    images_description = models.TextField(blank=True, null=True, help_text="Optional description of the image.")
    created_at = models.DateTimeField(auto_now_add=True,)
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
        return f"Classrooms for {self.school.name if self.school else 'Unknown School'}"

class Library(SchoolRelatedModel):
    """
    Stores library details. 
    """
    book_count = models.PositiveIntegerField(default=0)
    digital_access = models.BooleanField(default=False)
    study_space_capacity = models.PositiveIntegerField(blank=True, null=True)
    library_availability = models.TextField(blank=True)

    def __str__(self):
        return f"Library for {self.school.name if self.school else 'Unknown School'}"

class Laboratory(SchoolRelatedModel):
    """
    Stores laboratory details.
    """
    lab_type = models.CharField(max_length=100, choices=[
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Biology', 'Biology'),
        ('Robotics', 'Robotics'),
    ])
    lab_equipment = models.TextField(blank=True)
    lab_availability = models.TextField(blank=True)

    def __str__(self):
        return f"{self.lab_type} for {self.school.name if self.school else 'Unknown School'}"

class ComputerLab(SchoolRelatedModel):
    """
    Stores details about computer labs.
    """
    number_of_computers = models.PositiveIntegerField(default=0)
    internet_access = models.BooleanField(default=False)
    smart_classrooms = models.BooleanField(default=False)
    computer_lab_availability = models.TextField(blank=True)

    def __str__(self):
        return f"Computer Lab for {self.school.name if self.school else 'Unknown School'}"

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
        return f"Sports Facility for {self.school.name if self.school else 'Unknown School'}"

class VocationalFacility(SchoolRelatedModel):
    facility_name = models.CharField(max_length=100)
    facility_type = models.CharField(
        max_length=50,
        choices=[
            ("Workshop", "Workshop"),
            ("Laboratory", "Laboratory"),
            ("Training Center", "Training Center"),
        ],
    )
    description = models.TextField(blank=True)
    equipment_available = models.TextField(blank=True, help_text="List of equipment available.")
    capacity = models.PositiveIntegerField(blank=True, null=True, help_text="Capacity in terms of students or resources.")

    def __str__(self):
        return f"{self.facility_name} ({self.school.name})"

class SchoolImages(SchoolRelatedModel):
    """
    Stores images for various infrastructure types.
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    images_description = None
    image_type = models.CharField(max_length=50)
    image = models.ImageField(upload_to='infrastructure_images/%Y/%m/%d/')


    def save(self, *args, **kwargs):
        """
        Custom save method to rename the image file based on school name, image type, and original file name.
        """
        if self.image:
            # Generate a clean filename based on school name, image type, and original file name
            school_name_slug = slugify(self.school.name)  # Convert school name to a slug (e.g., "Test School" -> "test-school")
            image_name, extension = os.path.splitext(self.image.name)  # Split original file name and extension
            new_filename = f"{school_name_slug}_{self.image_type}_{image_name}{extension}"

            # Update the image name before saving
            self.image.name = new_filename

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.image_type.capitalize()} Image for {self.school.name if self.school else 'Unknown School'}"


@receiver(post_delete, sender=SchoolImages)
def delete_image_file_on_delete(sender, instance, **kwargs):
    """
    Signal description: Deletes image file from storage when a SchoolImages instance is deleted.
    """
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


@receiver(pre_save, sender=SchoolImages)
def delete_image_file_on_update(sender, instance, **kwargs):
    """
    Signal description: Deletes old image file when a new image is uploaded for an existing SchoolImages instance.
    """
    if instance.pk:
        old_instance = SchoolImages.objects.filter(pk=instance.pk).first()
        if old_instance and old_instance.image and old_instance.image != instance.image:
            if os.path.isfile(old_instance.image.path):
                os.remove(old_instance.image.path)

class SpecialNeedsResource(SchoolRelatedModel):
    """ 
    Special Needs Resources for schools: This model will allow schools to list their
     resource needs, making it easier for NGOs, government agencies, 
     or individuals to identify opportunities for support.
    """
    RESOURCE_CATEGORY_CHOICES = [
        ('furniture', 'Furniture'),
        ('equipment', 'Equipment'),
        ('facility', 'Facility'),
        ('educational_material', 'Educational Material'),
        ('technology', 'Technology'),
        ('other', 'Other'),
    ]

    resource_name = models.CharField(max_length=100, help_text="Name of the needed resource (e.g., Computers, Desks).")
    category = models.CharField(max_length=50, choices=RESOURCE_CATEGORY_CHOICES, help_text="Category of the resource.")
    quantity = models.PositiveIntegerField(help_text="Required quantity (e.g., 20 desks).")
    description = models.TextField(blank=True, help_text="Additional details about the resource needed.")
    urgency_level = models.CharField(
        max_length=50,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
        ],
        default='medium',
        help_text="Urgency level of the resource requirement.",
    )
    date_requested = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.resource_name} ({self.school.name})"

