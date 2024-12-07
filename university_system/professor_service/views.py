from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Professor, CourseAssignment
from .serializers import ProfessorSerializer, CourseAssignmentSerializer
from .service_clients import StudentServiceClient

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    lookup_field = 'professor_id'

    @action(detail=True, methods=['get'])
    def assignments(self, request, professor_id=None):
        professor = self.get_object()
        assignments = professor.assignments.all()
        serializer = CourseAssignmentSerializer(assignments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def course_students(self, request, professor_id=None):
        professor = self.get_object()
        course_id = request.query_params.get('course_id')
        
        if not course_id:
            return Response(
                {"error": "course_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            students = StudentServiceClient.get_course_students(course_id)
            return Response(students)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CourseAssignmentViewSet(viewsets.ModelViewSet):
    queryset = CourseAssignment.objects.all()
    serializer_class = CourseAssignmentSerializer