from django.db import models
from backend.schools.models import AcademicSession, SubjectRepository
from students.models import Student

class ExamMetadata(models.Model):
    """
    Metadata for exams, centralizing all exam-related details.
    """
    EXAM_TYPE_CHOICES = [
        ('midterm', 'Midterm Exam'),
        ('final', 'Final Exam'),
        ('continuous_assessment', 'Continuous Assessment'),
        ('mock', 'Mock Exam'),
        ('external', 'External Exam'),
    ]

    exam_type = models.CharField(
        max_length=30,
        choices=EXAM_TYPE_CHOICES,
        help_text="Type of the exam (e.g., Midterm, Final)."
    )
    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name="exams",
        help_text="The academic session this exam is part of."
    )
    exam_date = models.DateField(help_text="The date the exam is conducted.")
    subject = models.ForeignKey(
        SubjectRepository,
        on_delete=models.CASCADE,
        related_name="exams",
        help_text="The subject this exam is for."
    )
    max_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100.00,
        help_text="The maximum achievable score for the exam."
    )
    description = models.TextField(
        blank=True,
        help_text="Additional details or remarks about the exam."
    )

    class Meta:
        unique_together = ('exam_type', 'academic_session', 'subject')
        ordering = ['exam_date']

    def __str__(self):
        return f"{self.exam_type.capitalize()} - {self.subject.subject_name} ({self.academic_session.session_name})"



class ExaminationRecord(models.Model):
    """
    Tracks examination records for a student.
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="examination_records",
        help_text="The student this examination record is associated with."
    )
    subject = models.ForeignKey(
        'schools.SubjectRepository',
        on_delete=models.CASCADE,
        related_name="examination_records",
        help_text="The subject this examination is for."
    )
    
    # include CONTINUOUS ASSESSMENT SCORE
    score = models.DecimalField(max_digits=5, decimal_places=2, help_text="Score achieved in the exam.")
    grade = models.CharField(max_length=2, help_text="Grade achieved in the examination.")
    teacher_remarks = models.TextField(blank=True, help_text="Additional comments about the exam.")

    def __str__(self):
        return f"Exam: {self.student.full_name} ({self.subject.subject_name})"

