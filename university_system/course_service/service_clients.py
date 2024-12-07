import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError

class ProfessorServiceClient:
    BASE_URL = "http://localhost:8003/api"

    @classmethod
    def get_course_professors(cls, course_id):
        try:
            response = requests.get(f"{cls.BASE_URL}/assignments/", 
                                  params={'course_id': course_id})
            return response.json()
        except requests.RequestException as e:
            raise ValidationError(f"Could not fetch professors: {str(e)}")

class StudentServiceClient:
    BASE_URL = "http://localhost:8001/api"

    @classmethod
    def get_course_students(cls, course_id):
        try:
            response = requests.get(f"{cls.BASE_URL}/registrations/", 
                                  params={'course_id': course_id})
            return response.json()
        except requests.RequestException as e:
            raise ValidationError(f"Could not fetch students: {str(e)}")