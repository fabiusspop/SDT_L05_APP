# Service Registry Configuration
SERVICE_REGISTRY = {
    'SERVICES': {
        'STUDENT_SERVICE': {
            'name': 'student-service',
            'base_url': 'http://localhost:8001/api/',
            'health_check_url': 'http://localhost:8001/health/',
            'routes': [
                '/students/*',
                '/registrations/*'
            ]
        },
        'COURSE_SERVICE': {
            'name': 'course-service', 
            'base_url': 'http://localhost:8002/api/',
            'health_check_url': 'http://localhost:8002/health/',
            'routes': [
                '/courses/*',
                '/curricula/*'
            ]
        },
        'PROFESSOR_SERVICE': {
            'name': 'professor-service',
            'base_url': 'http://localhost:8003/api/',
            'health_check_url': 'http://localhost:8003/health/',
            'routes': [
                '/professors/*',
                '/assignments/*'
            ]
        },
        'GRADING_SERVICE': {
            'name': 'grading-service',
            'base_url': 'http://localhost:8004/api/',
            'health_check_url': 'http://localhost:8004/health/',
            'routes': [
                '/grades/*',
                '/disputes/*'
            ]
        }
    },
    'REGISTRY_UPDATE_INTERVAL': 30,  # seconds
    'SERVICE_TIMEOUT': 5,  # seconds
    'CIRCUIT_BREAKER': {
        'FAILURE_THRESHOLD': 5,
        'RESET_TIMEOUT': 60,  # seconds
        'RETRY_TIMEOUT': 30   # seconds
    }
} 