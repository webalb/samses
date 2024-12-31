from django.db import models

from .school import School

class Stakeholder(models.Model):
    """
    Model for school stakeholders (e.g., principal, liaison officer).
    """
    school = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        related_name='stakeholders',
        help_text="The school this stakeholder is associated with."
    )
    name = models.CharField(max_length=100, help_text="Name of the stakeholder.")
    position = models.CharField(
        max_length=100,
        choices=[
            ('Principal', 'Principal'),
            ('Liaison Officer', 'Liaison Officer'),
            ('Director', 'Director'),
            ('Board Member', 'Board Member'),
            ('Head Master', 'Head Master'),

        ],
        help_text="Position or role of the stakeholder."
    )
    email = models.EmailField(blank=True, null=True, help_text="Email address of the stakeholder.")
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text="Contact phone number.")
    tenure_start = models.DateField(help_text="Date when the stakeholder's tenure started.")
    tenure_end = models.DateField(blank=True, null=True, help_text="Date when the stakeholder's tenure ends (if applicable).")
    profile_picture = models.ImageField(upload_to='stakeholders_profiles/%Y/%m/%d/', blank=True, null=True, help_text="Profile picture of the stakeholder.")

    def __str__(self):
        return f"{self.name} - {self.position} ({self.school.name})"
class Staff(models.Model):
    """
    General model for school staff members.
    """
    POSITION_CHOICES = [
        ('Teacher', 'Teacher'),
        ('Assistant Teacher', 'Assistant Teacher'),
        ('Head Teacher', 'Head Teacher'),
        ('Form Master', 'Form Master'),
        ('Accountant', 'Accountant'),
        ('Clerk', 'Clerk'),
        ('Cleaner', 'Cleaner'),
        ('Security Guard', 'Security Guard'),
        ('Librarian', 'Librarian'),
        ('Counselor', 'Counselor'),
        ('ICT Officer', 'ICT Officer'),
        ('Lab Technician', 'Lab Technician'),
        ('Nurse', 'School Nurse'),
        ('Cafeteria Manager', 'Cafeteria Manager'),
        ('Driver', 'Driver'),
        ('Principal', 'Principal'),
        ('Vice Principal', 'Vice Principal'),
        ('Games Master', 'Games Master'),
        ('Administrative Officer', 'Administrative Officer'),
        ('Store Keeper', 'Store Keeper'),
        ('Nanny', 'Nanny'),
        ('Other', 'Other'),
    ]

    school = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        related_name='staffs',
        help_text="The school this staff member belongs to."
    )
    full_name = models.CharField(max_length=100, help_text="Full name of the staff member.")
    position = models.CharField(
        max_length=50,
        choices=POSITION_CHOICES,
        help_text="Job position of the staff member."
    )
    email = models.EmailField(blank=True, null=True, help_text="Email address of the staff member.")
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text="Contact phone number.")
    is_active = models.BooleanField(default=True, help_text="Indicates if the staff member is currently active.")
    date_joined = models.DateField(help_text="Date the staff member joined the school.")
    salary_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Monthly salary of the staff member.")
    profile_picture = models.ImageField(upload_to='staff_profiles/%Y/%m/%d/', blank=True, null=True, help_text="Profile picture of the staff member.")

    def __str__(self):
        return f"{self.full_name} ({self.get_position_display()}) - {self.school.name}"
