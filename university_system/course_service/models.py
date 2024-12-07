from django.db import models

class Course(models.Model):
    course_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    credits = models.IntegerField()
    department = models.CharField(max_length=100)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('ARCHIVED', 'Archived')
    ], default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course_id} - {self.title}"

class Curriculum(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    department = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course, through='CurriculumCourse')
    status = models.CharField(max_length=20, choices=[
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive')
    ], default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CurriculumCourse(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.IntegerField()  # Which semester this course should be taken
    is_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('curriculum', 'course')