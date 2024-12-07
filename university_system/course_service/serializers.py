from rest_framework import serializers
from .models import Course, Curriculum, CurriculumCourse

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CurriculumCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumCourse
        fields = '__all__'

class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = '__all__'