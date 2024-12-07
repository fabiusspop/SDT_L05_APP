import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError

class CourseServiceClient:
    BASE_URL = "http://localhost:8002/api"  # Course service URL

    @classmethod
    def validate_course(cls, course_id):
        try:
            response = requests.get(f"{cls.BASE_URL}/courses/{course_id}/")
            if response.status_code == 404:
                raise ValidationError(f"Course {course_id} does not exist")
            return response.json()
        except requests.RequestException as e:
            raise ValidationError(f"Could not validate course: {str(e)}")

class StudentServiceClient:
    BASE_URL = "http://localhost:8001/api"  # Student service URL

    @classmethod
    def get_course_students(cls, course_id):
        try:
            response = requests.get(f"{cls.BASE_URL}/registrations/", 
                                  params={'course_id': course_id})
            return response.json()
        except requests.RequestException as e:
            raise ValidationError(f"Could not fetch students: {str(e)}")