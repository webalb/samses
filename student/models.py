import os
import re
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import (
    EmailValidator,
    RegexValidator,
    MinLengthValidator,
    FileExtensionValidator,
)
from datetime import date

from schools.models import School


# Custom validator for text fields
def alphabet_space_hyphen_validator(value):
    if not re.match(r'^[a-zA-Z\s-]+$', value):
        raise ValidationError('This field can only contain alphabets, spaces, and hyphens.')

def validate_image(image):
    # Check file size
    max_size = 1 * 1024 * 1024  # 5 MB
    if image.size > max_size:
        raise ValidationError(f"Image file too large ( > {max_size} bytes )")
    return image

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(
        max_length=25,
        validators=[
            MinLengthValidator(2),
            alphabet_space_hyphen_validator
        ]
    )
    last_name = models.CharField(
        max_length=25,
        validators=[
            MinLengthValidator(2),
            alphabet_space_hyphen_validator
        ]
    )
    middle_name = models.CharField(
        max_length=25,
        blank=True,
        validators=[alphabet_space_hyphen_validator]
    )
    nin_number = models.PositiveIntegerField(max_length=11, blank=True, null=True, help_text="Student's NIN Number (optional).")

    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    country_of_birth = models.CharField(
        max_length=25,
        validators=[
            MinLengthValidator(2),
            alphabet_space_hyphen_validator
        ]
    )
    state_of_origin = models.CharField(
        max_length=25,
        validators=[
            MinLengthValidator(2),
            alphabet_space_hyphen_validator
        ]
    )
    place_of_birth = models.CharField(
        max_length=25,
        validators=[
            MinLengthValidator(2),
            alphabet_space_hyphen_validator
        ]
    )
    address = models.TextField(blank=True, null=True, help_text="Home address of the student.")

    email = models.EmailField(
        blank=True,
        null=True,
        validators=[EmailValidator()],
        help_text="Student's phone number (optional).",
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^(?:\+234|0)?[789]\d{9}$',
                message="Please use a valid Nigeria phone number"
            )
        ]
    )

    passport_photograph = models.ImageField(
        upload_to='students/passport/%Y/%m/%d/',
        unique=True,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png']),
            validate_image
            ]
    )

    school = models.ForeignKey(
        'School',
        on_delete=models.SET_NULL,
        related_name="students",
        help_text="The school this student is registered to.",
    )

    # Metadata
    is_active = models.BooleanField(default=True, help_text="Indicates if the student is currently active.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Record creation timestamp.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Record last updated timestamp.")

    class Meta:
        unique_together = (('first_name', 'last_name', 'date_of_birth'),)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()
    
    @property
    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age

    def save(self, *args, **kwargs):
        # Check if a new passport_photograph file is uploaded and update its name
        if self.pk and self.passport_photograph:
           
            try:
                old_passport_photograph = Student.objects.get(pk=self.pk).passport_photograph
            except Student.DoesNotExist:
                old_passport_photograph = None
            
            if old_passport_photograph and self.passport_photograph != old_passport_photograph:
                from schools.utils import remove_old_file
                if not remove_old_file(old_passport_photograph.path):
                    # Handle the case where file removal failed
                    import logging
                    logger.warning("Failed to remove old passport photograph file.")  

        super().save(*args, **kwargs)


class AdmissionInfo(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="admission_info",
        help_text="The student this admission info is associated with.",
    )
    school = models.ForeignKey(
        'School',
        on_delete=models.SET_NULL,
        related_name="admitted_students",
        help_text="The school this student is admitted to.",
    )
    admission_number = models.CharField(
        max_length=20, unique=True, help_text="Unique admission number."
    )
    admission_date = models.DateField(help_text="Date of admission.")
    program_level = models.ForeignKey(
        'schools.ProgramLevelTemplate',
        on_delete=models.SET_NULL,
        related_name="admitted_students",
        null=True,
        help_text="The level at which the student was admitted.",
    )
    def save(self, *args, **kwargs):
        if not self.admission_number:
            self.admission_number = self.generate_unique_admission_number()
        super().save(*args, **kwargs)

    def generate_unique_admission_number(self):
        while True:
            admission_number = str(uuid.uuid4().int)[:11]  # Get first 11 characters of UUID
            if not AdmissionInfo.objects.filter(admission_number=admission_number).exists():
                return admission_number
    def __str__(self):
        return f"Admission Info: {self.student.get_full_name()} ({self.school.name})"

class Guardian(models.Model):
    RELATIONSHIP_CHOICES = [
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Guardian', 'Guardian'),
        ('Grandfather', 'Grandfather'),
        ('Grandmother', 'Grandmother'),
        ('Uncle', 'Uncle'),
        ('Aunt', 'Aunt'),
        ('Brother', 'Brother'),
        ('Sister', 'Sister'),
        ('Other', 'Other'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="guardians",
        help_text="The student this guardian is associated with.",
    )
    full_name = models.CharField(max_length=100, help_text="Guardian's full name.")
    relationship = models.CharField(
        max_length=50,
        choices=RELATIONSHIP_CHOICES,
        default='Father',
        help_text="Relationship to the student (e.g., Father, Mother, Uncle).",
    )
    mark_as_emergency = models.BooleanField(default=True, help_text="Consider this guardian as emergency contact guardian.")
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^(?:\+234|0)?[789]\d{9}$',
            message="Please use a valid Nigeria phone number"
            )],
        help_text="Guardian's phone number.",
    )
    email = models.EmailField(blank=True, null=True, help_text="Guardian's email address (optional).")
    address = models.TextField(blank=True, null=True, help_text="Guardian's address.")

    def __str__(self):
        return f"{self.full_name} ({self.relationship} of {self.student.full_name})"

class AcademicInfo(models.Model):
    student = models.OneToOneField(
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

    def __str__(self):
        return f"Academic Info: {self.student.full_name} ({self.program_level})"

class Transfer(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="transfers",
        help_text="The student being transferred.",
    )
    transfer_type = models.CharField(
        max_length=50,
        choices=[
            ('intra_state', 'Intra-State Transfer'),
            ('inter_state', 'Inter-State Transfer'),
            ('from_samses', 'From Another SAMSES School'),
            ('non_samses', 'From Non-SAMSES School'),
        ],
        help_text="Type of transfer.",
    )
    from_school = models.ForeignKey(
        'schools.School',
        on_delete=models.SET_NULL,
        related_name="transferred_out_students",
        blank=True,
        null=True,
        help_text="The school the student is transferring from (if applicable).",
    )
    to_school = models.ForeignKey(
        'schools.School',
        on_delete=models.SET_NULL,
        related_name="transferred_in_students",
        blank=True,
        null=True,
        help_text="The school the student is transferring to (if applicable).",
    )
    transfer_date = models.DateField(help_text="Date of transfer.")
    remarks = models.TextField(blank=True, help_text="Additional details about the transfer.")

    def __str__(self):
        return f"Transfer: {self.student.full_name} ({self.transfer_type})"

from django.db import models
from schools.models import School, AcademicSession, LevelClasses, Stream
from students.models import Student

class EnrollmentRecord(models.Model):
    """
    Stores details about a student's enrollment for each academic session.
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollment_records",
        help_text="The student this enrollment record is associated with."
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="student_enrollments",
        help_text="The school the student is enrolled in."
    )
    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name="enrolled_students",
        help_text="The academic session this enrollment is for."
    )
    program_level = models.ForeignKey(
        LevelClasses,
        on_delete=models.CASCADE,
        related_name="enrolled_students",
        help_text="The level/class section the student is enrolled in."
    )
    stream = models.ForeignKey(
        Stream,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="enrolled_students",
        help_text="The stream the student is enrolled in (if applicable)."
    )
    enrollment_date = models.DateField(auto_now_add=True, help_text="Date of enrollment.")
    is_active = models.BooleanField(default=True, help_text="Indicates if this enrollment is currently active.")

    class Meta:
        unique_together = ('student', 'academic_session')

    def __str__(self):
        return f"Enrollment: {self.student.get_full_name()} ({self.academic_session.session_name})"
class AttendanceRecord(models.Model):
    """
    Tracks attendance for each student by subject and date.
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance_records",
        help_text="The student this attendance record is associated with."
    )
    subject = models.ForeignKey(
        'schools.SubjectRepository',
        on_delete=models.CASCADE,
        related_name="attendance_records",
        help_text="The subject this attendance record is for."
    )
    date = models.DateField(help_text="Date of attendance.")
    status = models.CharField(
        max_length=20,
        choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Excused', 'Excused')],
        default='Present',
        help_text="Attendance status for the student."
    )
    remarks = models.TextField(blank=True, help_text="Additional details about the attendance.")

    def __str__(self):
        return f"Attendance: {self.student.get_full_name()} ({self.date}) - {self.status}"
class AcademicPerformance(models.Model):
    """
    Stores details about a student's performance in a subject.
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="academic_performances",
        help_text="The student this performance record is associated with."
    )
    subject = models.ForeignKey(
        'schools.SubjectRepository',
        on_delete=models.CASCADE,
        related_name="performance_records",
        help_text="The subject this performance record is for."
    )
    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name="performance_records",
        help_text="The academic session this performance record is for."
    )
    grade = models.CharField(max_length=2, help_text="Grade achieved by the student.")
    score = models.DecimalField(max_digits=5, decimal_places=2, help_text="Score achieved by the student.")
    remarks = models.TextField(blank=True, help_text="Additional comments on performance.")

    def __str__(self):
        return f"Performance: {self.student.get_full_name()} ({self.subject.subject_name})"

class AcademicProgression(models.Model):
    """
    Tracks a student's academic progression between levels and sessions.
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="progression_records",
        help_text="The student this progression record is associated with."
    )
    from_program_level = models.ForeignKey(
        LevelClasses,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="progressions_from",
        help_text="The level the student is progressing from."
    )
    to_program_level = models.ForeignKey(
        LevelClasses,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="progressions_to",
        help_text="The level the student is progressing to."
    )
    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.SET_NULL,
        related_name="progression_records",
        help_text="The academic session this progression record is for."
    )
    progression_date = models.DateField(auto_now_add=True, help_text="Date of progression.")

    def __str__(self):
        return f"Progression: {self.student.full_name} ({self.from_program_level} -> {self.to_program_level})"

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
    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name="examination_records",
        help_text="The academic session this examination is for."
    )
    exam_date = models.DateField(help_text="Date of the examination.")

    # include CONTINUOUS ASSESSMENT SCORE
    score = models.DecimalField(max_digits=5, decimal_places=2, help_text="Score achieved in the exam.")
    grade = models.CharField(max_length=2, help_text="Grade achieved in the examination.")
    teacher_remarks = models.TextField(blank=True, help_text="Additional comments about the exam.")

    def __str__(self):
        return f"Exam: {self.student.get_full_name()} ({self.subject.subject_name})"

from django.db import models
from schools.models import AcademicSession, SubjectRepository
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

# next model