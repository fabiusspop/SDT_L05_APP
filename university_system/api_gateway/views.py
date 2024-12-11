from django.http import JsonResponse, HttpResponse
from django.conf import settings
import requests
from service_registry.registry import registry

class APIGateway:
    @staticmethod
    def route_request(request, path):
        # Find appropriate service for the path
        service_id = registry.get_route_service(path)
        if not service_id:
            return JsonResponse(
                {"error": "No service found for this path"}, 
                status=404
            )

        try:
            # Get service URL from registry
            service_url = registry.get_service_url(service_id)
            
            # Forward the request
            response = requests.request(
                method=request.method,
                url=f"{service_url.rstrip('/')}/{path.lstrip('/')}",
                data=request.body if request.method in ['POST', 'PUT', 'PATCH'] else None,
                headers={key: value for key, value in request.headers.items()
                        if key.lower() not in ['host', 'content-length']},
                params=request.GET,
                timeout=settings.SERVICE_REGISTRY['SERVICE_TIMEOUT']
            )
            
            # Return the response
            return HttpResponse(
                content=response.content,
                status=response.status_code,
                content_type=response.headers.get('Content-Type', 'application/json')
            )

        except ConnectionError as e:
            return JsonResponse(
                {"error": str(e)}, 
                status=503
            )
        except Exception as e:
            return JsonResponse(
                {"error": f"Gateway Error: {str(e)}"}, 
                status=500
            ) 