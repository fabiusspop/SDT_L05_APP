from django.contrib import admin
from .models import Student, CourseRegistration

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email')
    search_fields = ('student_id', 'first_name', 'last_name', 'email')

@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'course_id', 'registration_date', 'grade', 'status')
    list_filter = ('status',)
    search_fields = ('student__student_id', 'course_id')