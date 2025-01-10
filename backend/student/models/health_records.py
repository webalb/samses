from django.db import models
from .student import Student
from backend.schools.models import School

class HealthRecord(models.Model):
    """
    Stores health-related details such as chronic illnesses, allergies, and emergency instructions.
    """
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="health_record")
    chronic_illnesses = models.TextField(blank=True, help_text="Details of chronic illnesses (if any).")
    allergies = models.TextField(blank=True, help_text="Known allergies of the student.")
    emergency_instructions = models.TextField(blank=True, help_text="Special instructions for emergencies.")
    doctor_contact = models.CharField(max_length=100, blank=True, help_text="Emergency contact of the family doctor or clinic.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.full_name} - Health Record"



class HealthScreening(models.Model):
    """
    Logs results of periodic health check-ups.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="health_screenings")
    screening_date = models.DateField(help_text="Date of the health screening.")
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Height in cm.")
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Weight in kg.")
    vision = models.CharField(max_length=50, blank=True, help_text="Vision test result (e.g., 20/20).")
    hearing = models.CharField(max_length=50, blank=True, help_text="Hearing test result.")
    general_health = models.TextField(blank=True, help_text="Summary of overall health.")
    recommendations = models.TextField(blank=True, help_text="Health recommendations or follow-ups.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - Health Screening ({self.screening_date})"
