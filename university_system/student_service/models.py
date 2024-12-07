from django.db import models

# Create your models here.
class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"

class CourseRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='registrations')
    course_id = models.CharField(max_length=20)  # This will reference courses from Course Service
    registration_date = models.DateTimeField(auto_now_add=True)
    grade = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('REGISTERED', 'Registered'),
        ('COMPLETED', 'Completed'),
        ('DROPPED', 'Dropped')
    ])

    class Meta:
        unique_together = ('student', 'course_id')