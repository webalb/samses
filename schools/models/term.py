from django.db import models

from .academic_session import AcademicSession

class Term(models.Model):
    academic_session = models.OneToOneField(AcademicSession, on_delete=models.CASCADE, related_name='term_dates')
    start_date_1 = models.DateField(null=True, blank=True)
    end_date_1 = models.DateField(null=True, blank=True)
    start_date_2 = models.DateField(null=True, blank=True)
    end_date_2 = models.DateField(null=True, blank=True)
    start_date_3 = models.DateField(null=True, blank=True)
    end_date_3 = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Terms for {self.academic_session.session_name}"
