from django.db import models

class Grade(models.Model):
    student_id = models.CharField(max_length=20)  # References Student Service
    course_id = models.CharField(max_length=20)   # References Course Service
    professor_id = models.CharField(max_length=20) # References Professor Service
    
    grade_value = models.DecimalField(max_digits=4, decimal_places=2)
    grade_letter = models.CharField(max_length=2, choices=[
        ('A+', 'A+'), ('A', 'A'), ('A-', 'A-'),
        ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'),
        ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'),
        ('D+', 'D+'), ('D', 'D'), ('D-', 'D-'),
        ('F', 'F'),
    ])
    
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    submission_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    comments = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('APPROVED', 'Approved'),
        ('DISPUTED', 'Disputed'),
    ], default='DRAFT')

    class Meta:
        unique_together = ('student_id', 'course_id', 'semester', 'year')

    def __str__(self):
        return f"{self.student_id} - {self.course_id} - {self.grade_letter}"

class GradeDispute(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='disputes')
    reason = models.TextField()
    submitted_by = models.CharField(max_length=20)  # student_id
    submitted_date = models.DateTimeField(auto_now_add=True)
    resolution = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('UNDER_REVIEW', 'Under Review'),
        ('RESOLVED', 'Resolved'),
        ('REJECTED', 'Rejected'),
    ], default='PENDING')
    resolved_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Dispute - {self.grade} - {self.status}"