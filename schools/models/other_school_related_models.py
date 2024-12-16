import uuid

from django.db import models
from django.db.models import Q

from schools.models import School
from students.algorithms import generate_luhn_check_digit

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

		school_type_code = {
            'public': '1',
            'private': '2',
            'community': '3',
        }

		type_code = school_type_code[self.school.school_type]
		last_school = School.objects.filter(school_type=self.school.school_type).order_by('id').last()
		if not last_school:
			unique_code = '001'
		else:
			last_id = int(last_school.registration_number[4:])  # Get the numeric part of the last school ID
			unique_code = str(last_id + 1).zfill(3)
		last_digit = generate_luhn_check_digit(int(unique_code+type_code))
		return f"ACCR{str(date.today().year)[2:]}{type_code}{unique_code}{last_digit}"

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


class SuspensionClosure(models.Model):
    """
    Description:  Records of any suspensions or closures.          |
    """
    school = models.ForeignKey('School', on_delete=models.CASCADE)
    OPTIONS = [('Suspended', 'Suspension'), ('Closed', 'Closure')]
    suspension_type = models.CharField(max_length=100, choices=OPTIONS)
    reason = models.TextField()
    suspended_from = models.DateField()
    suspended_to = models.DateField(blank=True, null=True)
    is_indefinite = models.BooleanField(default=False)
    is_dropped = models.BooleanField(default=False,)
    date_created = models.DateTimeField(auto_now_add=True,)

    def save(self, *args, **kwargs):
	    if self.is_indefinite == True:
		    self.suspended_to = None
	    super().save(*args, **kwargs)


# Add models for: Level(1 to 6 for primary, 1 to 3 for jr, 1 to 3 for ss), Classes (to handle class 1A, 1B, 2C e.t.c.)
