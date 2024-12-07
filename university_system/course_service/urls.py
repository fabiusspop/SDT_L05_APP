from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, CurriculumViewSet, CurriculumCourseViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'curricula', CurriculumViewSet)
router.register(r'curriculum-courses', CurriculumCourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]