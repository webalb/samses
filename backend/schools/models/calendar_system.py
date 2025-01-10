from datetime import date

from django.db import models

from .school import School

class AcademicSession(models.Model):
    SCHOOL_TYPE_CHOICES = [
        ('all', 'All schools'),
        ('public', 'Public schools'),
        ('private', 'Private schools'),
        ('community', 'Community schools'),
        ('individual', 'Individual schools'),
    ]
    PROGRAM_CHOICES = [
        ('primary', 'Primary Schools'),
        ('jss', 'Junior Secondary Schools'),
        ('sss', 'Senior Secondary Schools'),
        ('primary+jss', 'Primary + Junior Secondary Schools'),
        ('jss+sss', 'Junior Secondary Schools + Senior Secondary Schools'),
        ('all', 'All Programs'),
    ]
 
    school_type = models.CharField(max_length=10, choices=SCHOOL_TYPE_CHOICES, default='all')
    program = models.CharField(max_length=12, choices=PROGRAM_CHOICES, default='all')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='academic_sessions', null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[  ("ongoing", "Ongoing"),
                   ("completed", "Completed"),
                   ("upcoming", "Upcoming"),
                ],
        default='upcoming',
        help_text="Current status of the academic session."
    )

    session_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        if self.school_type == 'all':
            return f"Session {self.session_name}, set for All schools, and for all {'programs' if self.program=='all' else self.program}"
        elif self.school_type == 'public':
            return f"Session {self.session_name} set for: All public schools, and for all {self.program}"
        elif self.school_type == 'private':
            return f"Session {self.session_name} set for: All private schools, and for all {self.program}"
        elif self.school_type == 'community':
            return f"Session {self.session_name} set for: All community schools, and for all {self.program}"
        elif self.school_type == 'individual':
            return f"Session {self.session_name} set for: {self.school.name}, and for its {self.program}" # type: ignore

    def complete_session(self):
        self.status = "completed"
        self.save()

    @classmethod
    def complete_all_ongoing_sessions(cls):
        cls.objects.filter(status="ongoing").update(status="completed")
        
    class Meta:
        unique_together = ('school', 'session_name', 'program', 'school_type')
        ordering = ['start_date']

    def duration(self):
        """
        Calculates the duration of the academic session in months and days.
        """
        delta = self.end_date - self.start_date
    

        return delta.days

    def duration_in_months(self):
        """
        Calculates the duration of the academic session in months and days.
        """
        delta = self.end_date - self.start_date
        months = delta.days // 30  # Approximate months
        remaining_days = delta.days % 30

        return f"{months} months and {remaining_days} days"

    def is_active(self):
        today = date.today()
        return self.start_date <= today <= self.end_date
    
    def on_coming(self):
        today = date.today()
        return today < self.start_date

    @property
    def schools(self):
        if self.school_type == 'individual':
            return self.school 
        else:
            return self.school_type 

    def get_term(self):
        return Term.objects.filter(academic_session=self)

    def get_current_term(self):
        """
        Returns the current Term object for the current date, 
        or None if no current term is found.
        """
        today = date.today()
        try:
            return self.terms.get(start_date__lte=today, end_date__gte=today) 
        except Term.DoesNotExist:
            return None

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Term(models.Model):
    academic_session = models.ForeignKey(
        'AcademicSession',
        on_delete=models.CASCADE,
        related_name='terms',
        help_text="The academic session this term belongs to."
    )
    term_name = models.PositiveSmallIntegerField(
        choices=[(1, 'First Term'), (2, 'Second Term'), (3, 'Third Term')],
        help_text="Name of the term."
    )
    start_date = models.DateField(null=True, help_text="Start date of the term.")
    end_date = models.DateField(null=True, help_text="End date of the term.")

    def clean(self):
        super().clean()

        # Validation 1: Ensure term_name is valid
        if self.term_name not in [1, 2, 3]:
            raise ValidationError(
                {'term_name': _("Term name must be (First Term), (Second Term), or (Third Term).")}
            )

        # Validation 2: Ensure start_date and end_date are not null
        if not self.start_date:
            raise ValidationError({'start_date': _("Start date is required.")})
        if not self.end_date:
            raise ValidationError({'end_date': _("End date is required.")})

        # Validation 3: Ensure start_date is before end_date
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError(
                {'end_date': _("End date must be after the start date.")}
            )

        # Validation 4: Ensure start_date and end_date fall within the academic session range
        if self.academic_session:
            if self.start_date < self.academic_session.start_date:
                raise ValidationError(
                    {'start_date': _("The term's start date cannot be before the start date of the academic session.")}
                )
            if self.end_date > self.academic_session.end_date:
                raise ValidationError(
                    {'end_date': _("The term's end date cannot be after the end date of the academic session.")}
                )

        # Validation 5: Ensure term_name is unique within an academic session
        if Term.objects.filter(
            academic_session=self.academic_session,
            term_name=self.term_name
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                {'term_name': _("A term with this name already exists for the selected academic session.")}
            )

        # Validation 6: Ensure no overlapping date ranges within the same academic session
        overlapping_terms = Term.objects.filter(
            academic_session=self.academic_session,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date
        ).exclude(pk=self.pk)
        if overlapping_terms.exists():
            raise ValidationError(
                _("The date range for this term overlaps with another term in the same academic session."),
                code='overlapping_dates'
            )

        # Validation 7: Ensure academic session is not None
        if not self.academic_session:
            raise ValidationError({'academic_session': _("An academic session is required.")})

    def save(self, *args, **kwargs):
        # Ensure clean is called before saving
        self.full_clean()  # Calls clean()
        super().save(*args, **kwargs)

    @property
    def status(self):
        today = date.today()
        if self.start_date > today:
            return "Not Started"
        elif self.end_date < today:
            return "Done"
        return "Active"

    def __str__(self):
        return f"{self.get_term_name_display()} - {self.academic_session.session_name}"

class CalendarEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('Academic', 'Academic'),
        ('Administrative', 'Administrative'),
        ('Extra-Curricular', 'Extra-Curricular'),
        ('Emergency', 'Emergency'),
        ('Exam', 'Exam'),
        ('Other', 'Other'),
    ]

    school = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        related_name='calendar_events',
        help_text="The school this event belongs to."
    )
    academic_session = models.ForeignKey(
        'AcademicSession',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
        help_text="Academic session this event belongs to (optional)."
    )

    event_name = models.CharField(max_length=100, help_text="Name of the event (e.g., Mid-Term Exam, PTA Meeting).")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, help_text="Type of the event.")
    start_date = models.DateTimeField(help_text="Start date and time of the event.")
    end_date = models.DateTimeField(help_text="End date and time of the event.")
    is_mandatory = models.BooleanField(default=True, help_text="Indicates if attendance is mandatory.")
    description = models.TextField(blank=True, help_text="Additional details about the event.")
    recurrence_type = models.CharField(
        max_length=20,
        choices=[
            ('None', 'None'),
            ('Weekly', 'Weekly'),
            ('Monthly', 'Monthly'),
            ('Yearly', 'Yearly')
        ],
        default='None',
        help_text="Indicates if the event recurs periodically."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_name} ({self.school.name})"

class SuspensionClosure(models.Model):
    """
    Description:  Records of any suspensions or closures.          |
    """
    school = models.ForeignKey('School', on_delete=models.CASCADE)
    is_statewide = models.BooleanField(default=False,)
    OPTIONS = [('Suspension', 'Suspension'), ('Closure', 'Closure')]
    suspension_type = models.CharField(max_length=100, choices=OPTIONS)
    reason = models.TextField()
    suspended_from = models.DateField()
    suspended_to = models.DateField(blank=True, null=True)
    is_indefinite = models.BooleanField(default=False)
    is_dropped = models.BooleanField(default=False,)

    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.is_indefinite == True:
            self.suspended_to = None
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{'State wide' if self.is_statewide else self.school.name} {self.suspension_type} ({self.start_date})"

    def affects_date(self, query_date):
        if self.is_dropped:
            return False
        if self.is_indefinite:
            return query_date >= self.suspended_from
        return self.suspended_from <= query_date <= self.suspended_to
