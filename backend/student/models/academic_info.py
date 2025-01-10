from django.db import models
from .student import Student
from backend.schools.models import School

class AcademicInfo(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="academic_info",
        help_text="The student this academic info is associated with.",
    )
    program_level = models.ForeignKey(
        'schools.ProgramLevelTemplate',
        on_delete=models.SET_NULL,
        related_name="academic_students",
        null=True,
        help_text="The current academic level of the student.",
    )
    class_section = models.ForeignKey(
        'schools.LevelClasses',
        on_delete=models.SET_NULL,
        related_name="academic_students",
        null=True,
        help_text="The current class section of the student.",
    )
    stream = models.ForeignKey(
        'schools.Stream',
        on_delete=models.SET_NULL,
        related_name="academic_students",
        blank=True,
        null=True,
        help_text="The stream the student belongs to (e.g., Science).",
    )
    academic_session = models.ForeignKey(
        'schools.AcademicSession',
        on_delete=models.SET_NULL,
        null=True,
        help_text="The academic session this enrollment is for."
    )
    progression_status = models.CharField(
        max_length=20,
        choices=[
            ('Promoted', 'Promoted'),
            ('Repeating', 'Repeating'),
            ('Graduated', 'Graduated'),
            ('Withdrawn', 'Withdrawn'),
            ('Transferred', 'Transferred'),
        ],
        default='Promoted',
        blank=True,
        null=True,
        help_text="The current academic progression status of the student."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Academic Info: {self.student.full_name} ({self.program_level})"

class EnrollmentRecord(models.Model):
    """
    Stores details about a student's enrollment for each academic session.
    """
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollment_record",
        help_text="The student this enrollment record is associated with."
    )
    # set student.school during enrollment capture
    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
        related_name="student_enrollments",
        help_text="The school the student is enrolled in."
    )
    program = models.CharField(max_length=10)
    # set school current academic session
    academic_session = models.ForeignKey(
        'schools.AcademicSession',
        on_delete=models.SET_NULL,
        null=True,
        related_name="enrolled_students",
        help_text="The academic session this enrollment is for."
    )

    # class level section.
    program_level = models.ForeignKey(
        'schools.LevelClasses',
        on_delete=models.SET_NULL,
        related_name="enrolled_students",
        null=True,
        help_text="The level/class section the student is enrolled in."
    )
    # for sss student
    stream = models.ForeignKey(
        'schools.Stream',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="enrolled_students",
        help_text="The stream the student is enrolled in (if applicable)."
    )
    enrollment_mode = models.CharField(
        max_length=1,
        choices=[
            ('1', 'Fresh enrollment'),
            ('2', 'Transfer'),
        ],
        default='1',
        help_text="Mode of enrollment for the student."
    )
    generate_admission_info = models.BooleanField(default=True, help_text="Generate admission information for this student.")
    enrollment_date = models.DateField(auto_now_add=True, help_text="Date of enrollment.")
    is_active = models.BooleanField(default=True, help_text="Indicates if this enrollment is currently active.")
    
    class Meta:
        unique_together = ('student', 'academic_session')

    def __str__(self):
        return f"Enrollment: {self.student.full_name} ({self.enrollment_mode})"
