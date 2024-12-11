from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Curriculum, CurriculumCourse
from .serializers import CourseSerializer, CurriculumSerializer, CurriculumCourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'course_id'

    @action(detail=True, methods=['get'])
    def prerequisites(self, request, course_id=None):
        course = self.get_object()
        prerequisites = course.prerequisites.all()
        serializer = CourseSerializer(prerequisites, many=True)
        return Response(serializer.data)

class CurriculumViewSet(viewsets.ModelViewSet):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer

    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        curriculum = self.get_object()
        courses = curriculum.courses.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class CurriculumCourseViewSet(viewsets.ModelViewSet):
    queryset = CurriculumCourse.objects.all()
    serializer_class = CurriculumCourseSerializer
    
# Add this to course_service/views.py to simulate failures
@action(detail=True, methods=['get'])
def test_circuit_breaker(self, request, course_id=None):
        # Simulate a service failure
        raise ConnectionError("Service temporarily unavailable")