from django.db import models

# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
from .service_clients import CourseServiceClient

class Professor(models.Model):
    professor_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    title = models.CharField(max_length=50, choices=[
        ('ASSISTANT', 'Assistant Professor'),
        ('ASSOCIATE', 'Associate Professor'),
        ('FULL', 'Full Professor'),
        ('EMERITUS', 'Professor Emeritus'),
    ])
    phone_number = models.CharField(max_length=20)
    office_location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.professor_id} - Dr. {self.last_name}"

class CourseAssignment(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='assignments')
    course_id = models.CharField(max_length=20)
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    status = models.CharField(max_length=20, choices=[
        ('SCHEDULED', 'Scheduled'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('professor', 'course_id', 'semester', 'year')