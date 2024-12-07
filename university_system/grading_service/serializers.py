from rest_framework import serializers
from .models import Grade, GradeDispute

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class GradeDisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeDispute
        fields = '__all__'