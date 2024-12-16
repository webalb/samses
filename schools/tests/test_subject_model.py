from django.test import TestCase
from django.db import IntegrityError
from schools.models import Subject, School

class SubjectModelTest(TestCase):

    def setUp(self):
        # Set up a test school
        self.school = School.objects.create(name="Test School", registration_number="MOE3004")
    
    def test_create_unique_subject(self):
        """ Test creating a subject with unique combination of name, program, general/specific, and optional """
        subject = Subject.objects.create(
            subject_name="Mathematics",
            program="primary",
            is_general=True,
            is_optional=False,
            school=self.school
        )
        self.assertEqual(subject.subject_name, "Mathematics")
        self.assertEqual(subject.program, "primary")
        self.assertEqual(subject.is_general, True)
        self.assertEqual(subject.is_optional, False)
    
    def test_create_duplicate_subject_raises_error(self):
        """ Test that duplicate subjects with the same combination cannot be created """
        # Create the first subject
        Subject.objects.create(
            subject_name="Mathematics",
            program="primary",
            is_general=True,
            is_optional=False,
        )
        
        # Try to create the same subject again and expect an IntegrityError due to the unique constraint
        with self.assertRaises(IntegrityError):
            Subject.objects.create(
                subject_name="Mathematics",
                program="primary",
                is_general=True,
                is_optional=False,
            )

    def test_create_different_subjects_for_same_school(self):
        """ Test that different subjects can be created for the same school """
        # Create multiple subjects with different names or properties
        subject1 = Subject.objects.create(
            subject_name="Mathematics",
            program="primary",
            is_general=True,
            is_optional=False,
            school=self.school
        )
        subject2 = Subject.objects.create(
            subject_name="Science",
            program="primary",
            is_general=True,
            is_optional=False,
            school=self.school
        )
        subject3 = Subject.objects.create(
            subject_name="English",
            program="primary",
            is_general=True,
            is_optional=False,
            school=self.school
        )

        self.assertEqual(Subject.objects.count(), 3)

    def test_create_subjects_with_different_programs(self):
        """ Test creating subjects with the same name but different programs should work """
        # Create subjects with the same name but different programs
        subject1 = Subject.objects.create(
            subject_name="Mathematics",
            program="primary",
            is_general=True,
            is_optional=False,
            school=self.school
        )
        subject2 = Subject.objects.create(
            subject_name="Mathematics",
            program="jss",
            is_general=True,
            is_optional=False,
            school=self.school
        )
        subject3 = Subject.objects.create(
            subject_name="Mathematics",
            program="sss",
            is_general=True,
            is_optional=False,
            school=self.school
        )

        self.assertEqual(Subject.objects.count(), 3)

    def test_create_subject_with_general_and_specific(self):
        """ Test creating subjects with the same name but marked as General or Specific """
        # Create a general subject
        subject1 = Subject.objects.create(
            subject_name="Mathematics",
            program="primary",
            is_general=True,
            is_optional=False,
            school=self.school
        )
        # Create a specific subject
        subject2 = Subject.objects.create(
            subject_name="Mathematics",
            program="primary",
            is_general=False,
            is_optional=False,
            school=self.school
        )
        
        self.assertEqual(Subject.objects.count(), 2)

    def test_create_optional_and_non_optional_subjects(self):
        """ Test creating a subject as optional and non-optional for the same combination """
        # Create a non-optional subject
        subject1 = Subject.objects.create(
            subject_name="Mathematics",
            program="primary",
            is_general=True,
            is_optional=False,
            school=self.school
        )
        # Create an optional subject
        subject2 = Subject.objects.create(
            subject_name="Mathematics",
            program="primary",
            is_general=True,
            is_optional=True,
            school=self.school
        )
        
        self.assertEqual(Subject.objects.count(), 2)

    def test_create_subject_for_all_schools(self):
        """ Test creating a subject for 'all' schools should be unique """
        # Create a subject for all schools
        subject1 = Subject.objects.create(
            subject_name="Mathematics",
            program="all",
            is_general=True,
            is_optional=False,
            school=None  # No specific school for "all"
        )
        # Try creating the same subject for all schools
        with self.assertRaises(IntegrityError):
            Subject.objects.create(
                subject_name="Mathematics",
                program="all",
                is_general=True,
                is_optional=False,
                school=None
            )

    def test_create_subject_for_specific_school(self):
        """ Test that subjects created for specific schools work as expected """
        # Create a subject for a specific school
        subject1 = Subject.objects.create(
            subject_name="Mathematics",
            program="primary",
            is_general=True,
            is_optional=False,
            school=self.school
        )
        # Create another subject for the same school but different program
        subject2 = Subject.objects.create(
            subject_name="Science",
            program="primary",
            is_general=True,
            is_optional=False,
            school=self.school
        )
        
        self.assertEqual(Subject.objects.count(), 2)

