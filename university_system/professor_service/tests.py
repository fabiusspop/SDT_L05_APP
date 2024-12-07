from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Professor, CourseAssignment

class ProfessorTests(APITestCase):
    def setUp(self):
        self.professor_data = {
            'professor_id': 'PROF001',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@university.edu',
            'department': 'Computer Science',
            'title': 'ASSISTANT',
            'phone_number': '123-456-7890',
            'office_location': 'Building A, Room 101'
        }

    def test_create_professor(self):
        response = self.client.post('/api/professors/', self.professor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Professor.objects.count(), 1)
        self.assertEqual(Professor.objects.get().professor_id, 'PROF001')