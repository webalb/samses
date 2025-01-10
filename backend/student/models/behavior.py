from django.db import models
from .student import Student
from .school import School

class BehaviorRecord(models.Model):
    """
    Logs student behavior incidents, including offense type, date, and resolution.
    """
    BEHAVIOR_TYPE_CHOICES = [
        ('minor', 'Minor Offense'),
        ('major', 'Major Offense'),
        ('severe', 'Severe Offense'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="behavior_records")
    school = models.ForeignKey(School, on_delete=models.SET_NULL, related_name="behavior_records")
    incident_date = models.DateField(help_text="Date of the incident.")
    offense_type = models.CharField(max_length=20, choices=BEHAVIOR_TYPE_CHOICES, help_text="Type of behavior offense.")
    description = models.TextField(help_text="Details about the behavior incident.")
    resolution = models.TextField(blank=True, help_text="Resolution or actions taken regarding the incident.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.get_offense_type_display()} ({self.incident_date})"


class DisciplinaryAction(models.Model):
    """
    Stores details of actions taken for discipline (e.g., warnings, suspensions, or counseling sessions).
    """
    ACTION_TYPE_CHOICES = [
        ('warning', 'Warning'),
        ('suspension', 'Suspension'),
        ('counseling', 'Counseling'),
        ('expulsion', 'Expulsion'),
        ('other', 'Other'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="disciplinary_actions")
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="disciplinary_actions")
    action_type = models.CharField(max_length=20, choices=ACTION_TYPE_CHOICES, help_text="Type of disciplinary action.")
    description = models.TextField(help_text="Details of the action taken.")
    action_date = models.DateField(help_text="Date the action was taken.")
    action_duration = models.PositiveIntegerField(blank=True, null=True, help_text="Duration of action in days (if applicable).")
    resolved = models.BooleanField(default=False, help_text="Indicates if the issue has been resolved.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.get_action_type_display()} ({self.action_date})"


class RecognitionRecord(models.Model):
    """
    Records awards, achievements, and commendations for behavior and performance.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="recognition_records")
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="recognition_records")
    award_name = models.CharField(max_length=100, help_text="Name of the award or recognition.")
    award_date = models.DateField(help_text="Date the award was given.")
    description = models.TextField(blank=True, help_text="Details about the recognition.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.award_name} ({self.award_date})"
