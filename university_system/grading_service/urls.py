from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GradeViewSet, GradeDisputeViewSet

router = DefaultRouter()
router.register(r'grades', GradeViewSet)
router.register(r'disputes', GradeDisputeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]