from django.db import models

from .student import Student

class Attendance(models.Model):
    """
    Tracks attendance for each student by subject and date.
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance_records",
        help_text="The student this attendance record is associated with."
    )
    date = models.DateField(help_text="Date of attendance.")
    status = models.CharField(
        max_length=20,
        choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Excused', 'Excused')],
        default='Present',
        help_text="Attendance status for the student."
    )

    def __str__(self):
        return f"Attendance: {self.student.get_full_name()} ({self.date}) - {self.status}"

