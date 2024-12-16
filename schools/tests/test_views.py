from django.test import TestCase, Client
from django.urls import reverse

from users.models import CustomUser as User
from schools.models import School
from schools.forms import SchoolForm
from django.core.files.uploadedfile import SimpleUploadedFile

class SchoolViewsTest(TestCase):
    def setUp(self):
        """
        Set up a test user, client, and initial data.
        """
        self.client = Client()
        self.admin_user = User.objects.create_user(username='admin', password='password123')
        self.school = School.objects.create(name="Test School", street_address="123 Test Street")
        self.client.login(username='admin', password='password123')

    def test_school_create_get(self):
        """
        Test the GET request for creating a school.
        """
        url = reverse('schools:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schools/school_create.html')
        self.assertIsInstance(response.context['form'], SchoolForm)

    def test_school_create_post_valid(self):
        """
        Test POST request for creating a school with valid data.
        """
        url = reverse('schools:create')
        school_data = {
            'name': 'New Test School',
            'address': '456 New Street',
            'logo': SimpleUploadedFile("logo.png", b"logo_content"),
        }
        response = self.client.post(url, school_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('schools:list'))
        self.assertEqual(School.objects.count(), 2)

    def test_school_create_post_invalid(self):
        """
        Test POST request for creating a school with invalid data.
        """
        url = reverse('schools:create')
        school_data = {
            'name': '',  # Invalid data (empty name)
            'address': 'Invalid Address',
        }
        response = self.client.post(url, school_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schools/school_create.html')
        self.assertFormError(response, 'form', 'name', 'This field is required.')

    def test_school_update_get(self):
        """
        Test the GET request for updating a school.
        """
        url = reverse('schools:update', args=[self.school.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schools/school_create.html')
        self.assertEqual(response.context['form'].instance, self.school)

    def test_school_update_post_valid(self):
        """
        Test the POST request for updating a school with valid data.
        """
        url = reverse('schools:update', args=[self.school.pk])
        updated_data = {
            'name': 'Updated School',
            'address': 'Updated Address',
        }
        response = self.client.post(url, updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('schools:details', args=[self.school.pk]))
        self.school.refresh_from_db()
        self.assertEqual(self.school.name, 'Updated School')

    def test_school_update_post_invalid(self):
        """
        Test the POST request for updating a school with invalid data.
        """
        url = reverse('schools:update', args=[self.school.pk])
        invalid_data = {
            'name': '',  # Invalid data
            'street_address': 'Updated Address',
        }
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schools/school_create.html')
        self.assertFormError(response, 'form', 'name', 'This field is required.')

    def test_school_list(self):
        """
        Test the school list view.
        """
        url = reverse('schools:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schools/school_list.html')
        self.assertIn(self.school, response.context['schools'])

    def test_school_details(self):
        """
        Test the school details view.
        """
        url = reverse('schools:details', args=[self.school.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schools/school_details.html')
        self.assertEqual(response.context['school'], self.school)

    def test_school_delete_get(self):
        """
        Test the GET request for confirming school deletion.
        """
        url = reverse('schools:delete', args=[self.school.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schools/school_confirm_delete.html')

    def test_school_delete_post(self):
        """
        Test the POST request for deleting a school.
        """
        url = reverse('schools:delete', args=[self.school.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('schools:list'))
        self.assertEqual(School.objects.count(), 0)
