from django.db import models
from .student import Student
from .school import School

class ClubMembership(models.Model):
    """
    Tracks students’ involvement in clubs, societies, and extracurricular groups.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="club_memberships")
    club_name = models.CharField(max_length=100, help_text="Name of the club or society.")
    role = models.CharField(max_length=50, blank=True, help_text="Role in the club (e.g., Member, President).")
    joined_date = models.DateField(help_text="Date when the student joined the club.")
    is_active = models.BooleanField(default=True, help_text="Indicates if the student is currently an active member.")

    def __str__(self):
        return f"{self.student.full_name} - {self.club_name} ({'Active' if self.is_active else 'Inactive'})"


class SportsParticipation(models.Model):
    """
    Logs participation in sports, including positions held and awards won.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="sports_participation")
    sport_name = models.CharField(max_length=100, help_text="Name of the sport.")
    position = models.CharField(max_length=50, blank=True, help_text="Position or role in the sport (e.g., Captain, Player).")
    awards = models.TextField(blank=True, help_text="Details of awards or recognitions received.")
    start_date = models.DateField(help_text="Start date of participation.")
    end_date = models.DateField(blank=True, null=True, help_text="End date of participation (if applicable).")

    def __str__(self):
        return f"{self.student.full_name} - {self.sport_name} ({self.position})"


class ActivityRecognition(models.Model):
    """
    Tracks recognitions received for extracurricular activities.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="activity_recognitions")
    activity_type = models.CharField(
        max_length=50,
        help_text="Type of activity (e.g., Club, Sport, Spelling)."
    )
    recognition_title = models.CharField(max_length=100, help_text="Title or name of the recognition.")
    description = models.TextField(blank=True, help_text="Details about the recognition.")
    date_awarded = models.DateField(help_text="Date when the recognition was awarded.")

    def __str__(self):
        return f"{self.student.full_name} - {self.recognition_title} ({self.activity_type.capitalize()})"
