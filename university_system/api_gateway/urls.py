from django.urls import path
from .views import APIGateway

urlpatterns = [
    path('<path:path>', APIGateway.route_request, name='api-gateway'),
] 