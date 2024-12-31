from django.test import TestCase
from schools.forms import SchoolForm

class SchoolFormTest(TestCase):
    def test_valid_form(self):
        """
        Test that a valid form with all required fields is valid.
        """
        data = {
            'name': 'Test School',
            'school_type': 'public', 
            'program': 'primary', 
            'lga': 'Test LGA',
            'ward': 'Test Ward',
            'street_address': '123 Test Street',
            'phone': '08012345678',
            'is_vocational': False,
            'established_date': '2023-11-28', 
        }
        form = SchoolForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_phone_number(self):
        """
        Test that the form is invalid with an invalid phone number.
        """
        data = {
            'name': 'Test School',
            'school_type': 'public', 
            'program': 'primary', 
            'lga': 'Test LGA',
            'ward': 'Test Ward',
            'street_address': '123 Test Street',
            'phone': '1234567', 
            'is_vocational': False,
            'established_date': '2023-11-28', 
        }
        form = SchoolForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
        self.assertEqual(form.errors['phone'][0], "Enter a valid Nigerian phone number.")

    def test_required_fields(self):
        """
        Test that required fields are correctly validated.
        """
        data = {}  # Empty data
        form = SchoolForm(data=data)
        self.assertFalse(form.is_valid())
        # Assert that all required fields have errors 
        # (You can add specific assertions for each required field)
