from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student, CourseRegistration
from .serializers import StudentSerializer, CourseRegistrationSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'student_id'

    @action(detail=True, methods=['get'])
    def grades(self, request, student_id=None):
        student = self.get_object()
        registrations = student.registrations.all()
        serializer = CourseRegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

class CourseRegistrationViewSet(viewsets.ModelViewSet):
    queryset = CourseRegistration.objects.all()
    serializer_class = CourseRegistrationSerializer
