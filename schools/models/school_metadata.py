from django.db import models
from .school import School
# School Academic Information.
class SchoolMetadata(models.Model):
 	"""Some Metadata options settings for schools."""
 	LANGUAGES = [
 					("en", "English"),
 					("hs", "Hausa"),
 					("ff", "Fulfulde"),
 					("yb", "Yoruba"),
 					("ig", "Igbo"),
 				]
 	school = models.OneToOneField(School, on_delete=models.CASCADE)
 	language_of_instruction = models.CharField(
 		max_length=2, 
 		choices=LANGUAGES, 
 		default=LANGUAGES[0],
 		help_text="Primary language(s) used in teaching",
 		)
 	enrollment_capacity = models.PositiveSmallIntegerField(blank=True, null=False,help_text="Annual enrollment capacity of the school.")
