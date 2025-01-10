from django.test import TestCase, Client
from backend.schools.models import School
from backend.schools.forms import SchoolForm
from users.models import User as User
class SchoolCreateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_login(self.user) 

    def test_school_create_get(self):
        response = self.client.get('/schools/create/') 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schools/school_create.html')
        self.assertIsInstance(response.context['form'], SchoolForm)

    def test_school_create_post_valid(self):
        data = {
            'name': 'Test School',
            'school_type': 'public',
            'program': 'primary',
            'lga': 'Test LGA',
            'ward': 'Test Ward',
            'street_address': '123 Test Street',
        }
        response = self.client.post('/schools/create/', data)
        self.assertEqual(response.status_code, 302)  # Redirect expected
        self.assertEqual(School.objects.count(), 1) 
        self.assertEqual(School.objects.get(name='Test School').name, 'Test School')

    def test_school_create_post_invalid(self):
        data = {
            # Missing required fields or invalid data
        }
        response = self.client.post('/schools/create/', data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], SchoolForm)
        self.assertTrue(len(response.context['form'].errors) > 0)

    def test_school_create_post_duplicate_name(self):
        # Create an existing school with the same name
        data = {
            'name': 'Duplicate School',
            'school_type': 'public',
            'program': 'primary',
            'lga': 'Test LGA',
            'ward': 'Test Ward',
            'street_address': '123 Test Street',
            # Add other required fields from your SchoolForm
        }
        School.objects.create(data) 

        response = self.client.post('/schools/create/', data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], SchoolForm)
        self.assertIn('name', response.context['form'].errors)

    def test_school_create_post_max_length_exceeded(self):
        # Assuming 'name' field has a max_length constraint
        long_name = 'x' * 256  # Exceeds potential max_length
        data = {
            'name': long_name,
            'school_type': 'public',
            'program': 'primary',
            'lga': 'Test LGA',
            'ward': 'Test Ward',
            'street_address': '123 Test Street',
            # Add other required fields from your SchoolForm
        }
        response = self.client.post('/schools/create/', data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], SchoolForm)
        self.assertIn('name', response.context['form'].errors)

    def test_school_create_post_invalid_file_type(self):
        # Assuming a field like 'logo' expects a specific file type
        data = {
            'name': 'Test School',
            'school_type': 'public',
            'program': 'primary',
            'lga': 'Test LGA',
            'ward': 'Test Ward',
            'street_address': '123 Test Street',
            # Add other required fields from your SchoolForm
            'logo': 'invalid_file.txt'  # Simulate an invalid file upload
        }
        response = self.client.post('/schools/create/', data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], SchoolForm)
        self.assertIn('logo', response.context['form'].errors)

# ===============================
# ||| Test School Update View |||
# ===============================

class SchoolUpdateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_login(self.user)
        data = {
            'name': 'Test School',
            'school_type': 'public',
            'program': 'primary',
            'lga': 'Test LGA',
            'ward': 'Test Ward',
            'street_address': '123 Test Street',
        }
        self.school = School.objects.create(data)

    def test_school_update_get(self):
        response = self.client.get(f'/schools/{self.school.pk}/update/') 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schools/school_create.html') 
        self.assertIsInstance(response.context['form'], SchoolForm) 
        self.assertEqual(response.context['form'].instance, self.school) 

    def test_school_update_post_valid(self):
        data = {
            'name': 'Updated Test School',
            'school_type': 'private',
            'program': 'primary',
            'lga': 'Test LGA',
            'ward': 'Test Ward',
            'street_address': '123 Test Street',
            # Add other fields and their updated values
        }
        response = self.client.post(f'/schools/{self.school.pk}/update/', data)
        self.assertEqual(response.status_code, 302)  # Redirect expected
        self.school.refresh_from_db()  # Refresh the school object
        self.assertEqual(self.school.name, 'Updated Test School')

    def test_school_update_post_invalid(self):
        data = {
            # Missing required fields or invalid data
        }
        response = self.client.post(f'/schools/{self.school.pk}/update/', data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], SchoolForm)
        self.assertTrue(len(response.context['form'].errors) > 0)

    def test_school_update_post_duplicate_name(self):
        # Create another school with the name we want to update to
        data = {
            'name': 'Duplicate School',
            'school_type': 'public',
            'program': 'primary',
            'lga': 'Test LGA',
            'ward': 'Test Ward',
            'street_address': '123 Test Street',
            # Add other required fields from your SchoolForm
        }
        School.objects.create(data)

        response = self.client.post(f'/schools/{self.school.pk}/update/', data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], SchoolForm)
        self.assertIn('name', response.context['form'].errors)

    def test_school_update_post_max_length_exceeded(self):
        # Assuming 'name' field has a max_length constraint
        long_name = 'x' * 256  # Exceeds potential max_length
        data = {
            'name': long_name,
            'school_type': 'public',
            'program': 'primary',
            'lga': 'Test LGA',
            'ward': 'Test Ward',
            'street_address': '123 Test Street',
            # Add other required fields from your SchoolForm
        }
        response = self.client.post(f'/schools/{self.school.pk}/update/', data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], SchoolForm)
        self.assertIn('name', response.context['form'].errors)

    def test_school_update_post_invalid_file_type(self):
        # Assuming a field like 'logo' expects a specific file type
        data = {
            'name': 'Updated Test School',
            'school_type': 'public',
            'program': 'primary',
            'lga': 'Test LGA',
            'ward': 'Test Ward',
            'street_address': '123 Test Street',
            # Add other required fields from your SchoolForm
            'logo': 'invalid_file.txt'  # Simulate an invalid file upload
        }
        response = self.client.post(f'/schools/{self.school.pk}/update/', data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], SchoolForm)
        self.assertIn('logo', response.context['form'].errors)

