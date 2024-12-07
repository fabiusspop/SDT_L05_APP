from django.contrib import admin
from .models import Professor, CourseAssignment

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('professor_id', 'first_name', 'last_name', 'email', 'department', 'title')
    search_fields = ('professor_id', 'first_name', 'last_name', 'email')
    list_filter = ('department', 'title')

@admin.register(CourseAssignment)
class CourseAssignmentAdmin(admin.ModelAdmin):
    list_display = ('professor', 'course_id', 'semester', 'year', 'status')
    list_filter = ('status', 'semester', 'year')
    search_fields = ('professor__professor_id', 'course_id')