from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, CourseRegistrationViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'registrations', CourseRegistrationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]