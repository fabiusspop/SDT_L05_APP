from django.contrib import admin
from .models import Course, Curriculum, CurriculumCourse

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'title', 'department', 'credits', 'status')
    search_fields = ('course_id', 'title', 'description')
    list_filter = ('department', 'status', 'credits')

@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'status')
    search_fields = ('name', 'description', 'department')
    list_filter = ('department', 'status')

@admin.register(CurriculumCourse)
class CurriculumCourseAdmin(admin.ModelAdmin):
    list_display = ('curriculum', 'course', 'semester', 'is_required')
    list_filter = ('semester', 'is_required')
    search_fields = ('curriculum__name', 'course__course_id')