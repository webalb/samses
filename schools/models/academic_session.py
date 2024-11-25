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
    session_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        if self.school_type == 'all':
            return f"Session {self.session_name}, set for All schools, and for all {self.program}"
        elif self.school_type == 'public':
            return f"Session {self.session_name} set for: All public schools, and for all {self.program}"
        elif self.school_type == 'private':
            return f"Session {self.session_name} set for: All private schools, and for all {self.program}"
        elif self.school_type == 'community':
            return f"Session {self.session_name} set for: All community schools, and for all {self.program}"
        elif self.school_type == 'individual':
            return f"Session {self.session_name} set for: {self.school.name}, and for its {self.program}" # type: ignore

    class Meta:
        unique_together = ('school', 'session_name')

    def duration(self):
        return (self.end_date - self.start_date).days

    def is_active(self):
        today = date.today()
        return self.start_date <= today <= self.end_date
    
    def on_coming(self):
        today = date.today()
        return today < self.start_date

    def get_term(self):
        return Term.objects.filter(academic_session=self)

