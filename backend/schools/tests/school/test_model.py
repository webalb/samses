from datetime import date
from django.test import TestCase
from django.db.utils import IntegrityError
from backend.schools.models import School
from unittest.mock import patch
from tempfile import NamedTemporaryFile


SCHOOL_TYPE_CHOICES = [
        ('public', 'Public School'),
        ('private', 'Private School'),
        ('community', 'Community School'),
    ]
PROGRAM_CHOICES = [
        ('primary', 'Primary'),
        ('jss', 'Junior Secondary School'),
        ('sss', 'Senior Secondary School'),
        ('primary+jss', 'Primary + Junior Secondary School'),
        ('jss+sss', 'Junior Secondary School + Senior Secondary School'),
        ('all', 'All Programs'),
    ]
class SchoolModelTest(TestCase):

    def setUp(self):
        # Initial setup for tests
        self.school_data = {
            'name': 'Test Public School',
            'school_type': 'public',
            'program': 'primary',
            'lga': 'Test LGA',
            'ward': 'Test Ward',
            'street_address': '123 Test Street',
        }

    def test_create_school_with_valid_data(self):
        """
        Test that a school instance is created successfully with valid data.
        """
        school = School.objects.create(**self.school_data)
        self.assertEqual(School.objects.count(), 1)
        self.assertEqual(school.name, self.school_data['name'])
        self.assertEqual(school.school_type, self.school_data['school_type'])

    def test_unique_registration_number_generated(self):
        """
        Test that a unique registration number is generated for each school.
        """
        school = School.objects.create(**self.school_data)
        self.assertTrue(school.registration_number.startswith("1"))
        self.assertEqual(School.objects.filter(registration_number=school.registration_number).count(), 1)

    def test_unique_registration_number_generated(self):
        """
        Test that a unique registration number is generated for each school using UUID.
        """
        school = School.objects.create(**self.school_data)
        self.assertTrue(school.registration_number.startswith("1"))  # Updated assertion
        self.assertEqual(len(school.registration_number), 8)  # Expect 10 characters (MOE + 7 digits)
        # No need to check for specific prefix like "GME" anymore
        self.assertEqual(School.objects.filter(registration_number=school.registration_number).count(), 1)
    def test_program_choices(self):
        """
        Test that program choices are correctly assigned.
        """
        for program in dict(PROGRAM_CHOICES).keys():
            self.school_data['program'] = program
            school = School.objects.create(**self.school_data)
            self.assertEqual(school.program, program)

    def test_school_type_choices(self):
        """
        Test that school type choices are correctly assigned.
        """
        for school_type in dict(SCHOOL_TYPE_CHOICES).keys():
            self.school_data['school_type'] = school_type
            school = School.objects.create(**self.school_data)
            self.assertEqual(school.school_type, school_type)

    def test_get_levels_and_classes(self):
        """
        Test fetching levels and classes associated with a school.
        """
        school = School.objects.create(**self.school_data)
        levels_and_classes = school.get_levels_and_classes()
        self.assertIn('classes', levels_and_classes)
        self.assertIn('program_levels', levels_and_classes)

    def test_status_property(self):
        """
        Test the status property for a school based on accreditation and suspension reports.
        """
        school = School.objects.create(**self.school_data)
        self.assertEqual(school.status, '-')  # No accreditation or suspension by default

    def test_recent_accreditation_status(self):
        """
        Test fetching the most recent accreditation status.
        """
        school = School.objects.create(**self.school_data)
        self.assertIsNone(school.recent_accreditation_status())


    def test_get_absolute_url(self):
        """
        Test that the get_absolute_url method returns the correct URL.
        """
        school = School.objects.create(**self.school_data)
        self.assertEqual(school.get_absolute_url(), f"/schools/{school.pk}/details/")
