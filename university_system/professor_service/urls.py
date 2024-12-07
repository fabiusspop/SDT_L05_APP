from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfessorViewSet, CourseAssignmentViewSet

router = DefaultRouter()
router.register(r'professors', ProfessorViewSet)
router.register(r'assignments', CourseAssignmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]