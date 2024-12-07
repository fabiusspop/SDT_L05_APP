import json
from django.http import JsonResponse
from requests.exceptions import RequestException

class ServiceCommunicationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except RequestException as e:
            return JsonResponse({
                'error': 'Service Communication Error',
                'detail': str(e)
            }, status=503)