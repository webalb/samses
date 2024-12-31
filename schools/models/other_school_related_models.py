import uuid

from django.db import models
from django.db.models import Q

from schools.models import School
from django.utils.safestring import mark_safe

from student.algorithms import generate_luhn_check_digit


# School Compliance and Accreditation Information
class AccreditationStatus(models.Model):

	accreditation_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
	school = models.ForeignKey('School', on_delete=models.CASCADE)
	ACCR_OPTIONS = [('awaiting accreditation.', 'Awaiting Accreditation.'), ('accreditated', 'Accreditated'), ('not-accreditated', 'Not Accreditated'), ('cancelled', 'Accreditation cancelled')]
	status = models.CharField(max_length=23, choices=ACCR_OPTIONS, default=ACCR_OPTIONS[0])
	valid_from = models.DateField(blank=True, null=True)
	valid_to = models.DateField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True,)


	# Generate Accreditation Number format- ACCR-YYYY-DDDD Y-year, D-any digit
	def generate_accreditation_number(self):
		from datetime import date

		import uuid

		school_type_code = {
            'public': '1',
            'private': '2',
            'community': '3',
        }

		type_code = school_type_code[self.school.school_type]
		
		return f"ACCR{str(date.today().year)[2:]}{type_code}-{str((uuid.uuid4().int))[:7]}"

	def save(self, *args, **kwargs):
		if self.status == 'accreditated':
			self.accreditation_number = self.generate_accreditation_number()
		if self.status == 'pending':
			self.valid_from = None
			self.valid_to = None
		super().save(*args, **kwargs)


class InspectionReport(models.Model):
    """
    Description: Summary of Ministry inspections and reports
    """
    school = models.ForeignKey('School', on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False,)
    findings = models.TextField()
    recommendations = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def recommendations_mk(self):
        import markdown  # Import the markdown library
        html = markdown.markdown(self.findings)
        return mark_safe(html)
    @property
    def findings_mk(self):
        import markdown  # Import the markdown library
        html = markdown.markdown(self.recommendations)
        return mark_safe(html) 
 

class ParentEngagement(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='parent_engagements')
    activity_name = models.CharField(max_length=100, help_text="Name of the activity (e.g., PTA Meeting).")
    activity_date = models.DateField(help_text="Date of the activity.")
    participants_count = models.PositiveIntegerField(help_text="Number of parents who participated.")

    def __str__(self):
        return f"{self.activity_name} hold on {self.activity_date}"
