import threading
import time
import requests
from django.conf import settings
from datetime import datetime, timedelta
from functools import wraps

class CircuitBreaker:
    def __init__(self, failure_threshold, reset_timeout):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF-OPEN
        self._lock = threading.Lock()

    def can_execute(self):
        with self._lock:
            if self.state == 'CLOSED':
                return True
            elif self.state == 'OPEN':
                if (datetime.now() - self.last_failure_time).seconds >= self.reset_timeout:
                    self.state = 'HALF-OPEN'
                    return True
                return False
            return True  # HALF-OPEN state allows one try

    def record_success(self):
        with self._lock:
            self.failures = 0
            self.state = 'CLOSED'

    def record_failure(self):
        with self._lock:
            self.failures += 1
            self.last_failure_time = datetime.now()
            if self.failures >= self.failure_threshold:
                self.state = 'OPEN'

class ServiceRegistry:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.services = {}
        self.last_check = {}
        self.circuit_breakers = {}
        self._load_services()
        self._initialize_circuit_breakers()
        self._start_health_check_thread()
    
    def _load_services(self):
        """Load services from settings"""
        registry_settings = getattr(settings, 'SERVICE_REGISTRY', {})
        self.services = registry_settings.get('SERVICES', {})
        
        for service_id, service in self.services.items():
            self.last_check[service_id] = {
                'status': 'UNKNOWN',
                'last_check': None
            }

    def _initialize_circuit_breakers(self):
        """Initialize circuit breakers for each service"""
        cb_settings = settings.SERVICE_REGISTRY['CIRCUIT_BREAKER']
        for service_id in self.services:
            self.circuit_breakers[service_id] = CircuitBreaker(
                cb_settings['FAILURE_THRESHOLD'],
                cb_settings['RESET_TIMEOUT']
            )
    
    def _start_health_check_thread(self):
        """Start background thread for health checks"""
        def health_check_loop():
            while True:
                self._check_services_health()
                time.sleep(settings.SERVICE_REGISTRY['REGISTRY_UPDATE_INTERVAL'])
        
        thread = threading.Thread(target=health_check_loop, daemon=True)
        thread.start()
    
    def _check_services_health(self):
        """Check health status of all registered services"""
        for service_id, service in self.services.items():
            try:
                response = requests.get(
                    service['health_check_url'],
                    timeout=settings.SERVICE_REGISTRY['SERVICE_TIMEOUT']
                )
                status = 'HEALTHY' if response.status_code == 200 else 'UNHEALTHY'
                self.circuit_breakers[service_id].record_success()
            except requests.RequestException:
                status = 'UNHEALTHY'
                self.circuit_breakers[service_id].record_failure()
            
            self.last_check[service_id] = {
                'status': status,
                'last_check': datetime.now()
            }
    
    def get_service_url(self, service_id):
        """Get base URL for a service with circuit breaker protection"""
        if service_id not in self.services:
            raise ValueError(f"Unknown service: {service_id}")
        
        circuit_breaker = self.circuit_breakers[service_id]
        if not circuit_breaker.can_execute():
            raise ConnectionError(f"Circuit breaker is open for {service_id}")
        
        service = self.services[service_id]
        status = self.last_check[service_id]['status']
        
        if status == 'UNHEALTHY':
            circuit_breaker.record_failure()
            raise ConnectionError(f"Service {service_id} is unhealthy")
            
        return service['base_url']
    
    def get_service_status(self, service_id):
        """Get current status of a service"""
        if service_id not in self.last_check:
            return 'UNKNOWN'
        return self.last_check[service_id]

    def get_route_service(self, path):
        """Get service for a given route path"""
        for service_id, service in self.services.items():
            for route in service['routes']:
                if self._match_route(route, path):
                    return service_id
        return None

    def _match_route(self, route_pattern, path):
        """Match a route pattern with a path"""
        if route_pattern.endswith('/*'):
            return path.startswith(route_pattern[:-1])
        return route_pattern == path

# Global registry instance
registry = ServiceRegistry() 