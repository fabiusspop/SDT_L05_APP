import requests
from rest_framework.exceptions import ValidationError

class StudentServiceClient:
    BASE_URL = "http://localhost:8001/api"

    @classmethod
    def validate_student(cls, student_id):
        try:
            response = requests.get(f"{cls.BASE_URL}/students/{student_id}/")
            if response.status_code == 404:
                raise ValidationError(f"Student {student_id} does not exist")
            return response.json()
        except requests.RequestException as e:
            raise ValidationError(f"Could not validate student: {str(e)}")

class CourseServiceClient:
    BASE_URL = "http://localhost:8002/api"

    @classmethod
    def validate_course(cls, course_id):
        try:
            response = requests.get(f"{cls.BASE_URL}/courses/{course_id}/")
            if response.status_code == 404:
                raise ValidationError(f"Course {course_id} does not exist")
            return response.json()
        except requests.RequestException as e:
            raise ValidationError(f"Could not validate course: {str(e)}")

class ProfessorServiceClient:
    BASE_URL = "http://localhost:8003/api"

    @classmethod
    def validate_professor(cls, professor_id):
        try:
            response = requests.get(f"{cls.BASE_URL}/professors/{professor_id}/")
            if response.status_code == 404:
                raise ValidationError(f"Professor {professor_id} does not exist")
            return response.json()
        except requests.RequestException as e:
            raise ValidationError(f"Could not validate professor: {str(e)}")