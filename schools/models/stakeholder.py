from django.db import models

from .school import School

class Stakeholder(models.Model):
    # Link to the school
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="stakeholders")
    
    # Stakeholder Information
    stakeholder_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, choices=[
        ('Principal', 'Principal'),
        ('Director', 'Director'),
        ('Liaison Officer', 'Liaison Officer'),
        ('Board Member', 'Board Member'),
        ('Trustee', 'Trustee'),
        ('Academic Staff', 'Academic Staff'),
        ('Non Academic Staff', 'Non-Academic Staff'),
    ])
    contact_phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    # staff_id = models.CharField(max_length=12, blank=True, null=True)
     # roles = models.CharField(max_length=100, choices=[('academic staffs choices and non academic staff choices')], blank=True, null=True)


    def __str__(self):
        return f"{self.stakeholder_name} - {self.position} at {self.school.name}"