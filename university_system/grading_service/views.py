from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Grade, GradeDispute
from .serializers import GradeSerializer, GradeDisputeSerializer
from .service_clients import StudentServiceClient, CourseServiceClient, ProfessorServiceClient

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def perform_create(self, serializer):
        # Validate that referenced entities exist
        StudentServiceClient.validate_student(serializer.validated_data['student_id'])
        CourseServiceClient.validate_course(serializer.validated_data['course_id'])
        ProfessorServiceClient.validate_professor(serializer.validated_data['professor_id'])
        serializer.save()

    @action(detail=False, methods=['get'])
    def student_grades(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {"error": "student_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        grades = Grade.objects.filter(student_id=student_id)
        serializer = self.get_serializer(grades, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def course_grades(self, request):
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response(
                {"error": "course_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        grades = Grade.objects.filter(course_id=course_id)
        serializer = self.get_serializer(grades, many=True)
        return Response(serializer.data)

class GradeDisputeViewSet(viewsets.ModelViewSet):
    queryset = GradeDispute.objects.all()
    serializer_class = GradeDisputeSerializer

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        dispute = self.get_object()
        resolution = request.data.get('resolution')
        if not resolution:
            return Response(
                {"error": "resolution is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        dispute.resolution = resolution
        dispute.status = 'RESOLVED'
        dispute.save()
        return Response(self.get_serializer(dispute).data)