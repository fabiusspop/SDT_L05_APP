from django.conf import settings
import requests
from rest_framework.exceptions import ValidationError
from service_registry.registry import registry
from functools import wraps

class ServiceClient:
    def __init__(self, service_id):
        self.service_id = service_id
    
    @property
    def base_url(self):
        return registry.get_service_url(self.service_id)
    
    def make_request(self, method, endpoint, **kwargs):
        try:
            url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ValidationError(f"Service request failed: {str(e)}")

    def fallback_response(self, endpoint):
        """Provide fallback response when service is unavailable"""
        if 'professors' in endpoint:
            return []  # Empty list of professors
        elif 'students' in endpoint:
            return []  # Empty list of students
        return None

    def with_circuit_breaker(self, method, endpoint, **kwargs):
        try:
            return self.make_request(method, endpoint, **kwargs)
        except (ValidationError, ConnectionError):
            return self.fallback_response(endpoint)

class ProfessorServiceClient(ServiceClient):
    def __init__(self):
        super().__init__('PROFESSOR_SERVICE')

    def get_course_professors(self, course_id):
        return self.with_circuit_breaker('GET', 'assignments/', 
                                       params={'course_id': course_id})

class StudentServiceClient(ServiceClient):
    def __init__(self):
        super().__init__('STUDENT_SERVICE')

    def get_course_students(self, course_id):
        return self.with_circuit_breaker('GET', 'registrations/',
                                       params={'course_id': course_id})