from django.contrib import admin
from .models import Grade, GradeDispute

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'course_id', 'professor_id', 'grade_letter', 'semester', 'year', 'status')
    list_filter = ('grade_letter', 'semester', 'year', 'status')
    search_fields = ('student_id', 'course_id', 'professor_id')

@admin.register(GradeDispute)
class GradeDisputeAdmin(admin.ModelAdmin):
    list_display = ('grade', 'submitted_by', 'submitted_date', 'status')
    list_filter = ('status', 'submitted_date')
    search_fields = ('grade__student_id', 'grade__course_id', 'submitted_by')