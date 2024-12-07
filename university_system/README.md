# University Management System - Microservices Architecture

## Project Overview
This project implements a university management system using a microservices architecture. The system consists of four independent services that handle different aspects of university management:

1. Student Management Service (Port 8001)
2. Professor Management Service (Port 8003)
3. Course Management Service (Port 8002)
4. Grading Service (Port 8004)

## Architecture
Each service:
- Runs independently
- Has its own database
- Communicates with other services via REST APIs
- Is built using Django and Django REST Framework

### Service Communication Diagram

┌───────────────────┐                  ┌───────────────────┐
│                   │                  │                   │
│  Student Service  │◄─────────────────│  Grading Service  │
│     (8001)       │                  │     (8004)        │
│                   │                  │                   │
└────────┬─────────┘                  └─────────┬─────────┘
         │                                      │
         │                                      │
         │                                      │
         │                                      │
         ▼                                      ▼
┌───────────────────┐                  ┌───────────────────┐
│                   │                  │                   │
│  Course Service   │◄─────────────────│ Professor Service │
│     (8002)       │                  │     (8003)        │
│                   │                  │                   │
└───────────────────┘                  └───────────────────┘

───► : Service calls/dependencies

### Apply migrations for each service
python manage.py migrate # For student service (default)
python manage.py migrate --database=professor_service
python manage.py migrate --database=course_service
python manage.py migrate --database=grading_service

## Service Details

### 1. Student Management Service (Port 8001)
Manages student-related operations.

#### Key Features:
- Student personal data management
- Course registration
- View grades

#### Main Endpoints:
- `GET /api/students/` - List all students
- `POST /api/students/` - Create new student
- `GET /api/students/{student_id}/` - Get student details
- `PUT /api/students/{student_id}/` - Update student details
- `GET /api/registrations/` - List course registrations

### 2. Professor Management Service (Port 8003)
Handles faculty-related operations.

#### Key Features:
- Professor personal data management
- Course assignments
- View assigned courses

#### Main Endpoints:
- `GET /api/professors/` - List all professors
- `POST /api/professors/` - Create new professor
- `GET /api/professors/{professor_id}/` - Get professor details
- `PUT /api/professors/{professor_id}/` - Update professor details
- `GET /api/assignments/` - List course assignments

### 3. Course Management Service (Port 8002)
Manages curriculum and course information.

#### Key Features:
- Course catalog management
- Curriculum management
- Prerequisites handling

#### Main Endpoints:
- `GET /api/courses/` - List all courses
- `POST /api/courses/` - Create new course
- `GET /api/courses/{course_id}/` - Get course details
- `GET /api/curricula/` - List curricula
- `GET /api/curriculum-courses/` - List curriculum courses

### 4. Grading Service (Port 8004)
Handles grade management and disputes.

#### Key Features:
- Grade submission
- Grade updates
- Grade disputes
- Grade retrieval

#### Main Endpoints:
- `GET /api/grades/` - List all grades
- `POST /api/grades/` - Submit new grade
- `GET /api/grades/student_grades/?student_id=X` - Get student's grades
- `GET /api/disputes/` - List grade disputes
- `POST /api/disputes/{id}/resolve/` - Resolve grade dispute


## Database Structure

Each service has its own database:
- `student_service.sqlite3`
- `professor_service.sqlite3`
- `course_service.sqlite3`
- `grading_service.sqlite3`

## Error Handling

The services implement comprehensive error handling:
- 400 Bad Request - Invalid data
- 404 Not Found - Resource not found
- 500 Internal Server Error - Server-side issues
- Service-specific validation errors

## Future Improvements

Planned enhancements:
1. Authentication and Authorization
2. Docker containerization
3. Frontend implementation
4. Service discovery
5. Asynchronous communication options
6. Caching layer
7. Rate limiting
8. Monitoring and logging

# Testing University Microservices via Web Browser

## Prerequisites
1. All services should be running:
   ```bash
   # Terminal 1
   python manage.py runserver 8001  # Student Service

   # Terminal 2
   python manage.py runserver 8002  # Course Service

   # Terminal 3
   python manage.py runserver 8003  # Professor Service

   # Terminal 4
   python manage.py runserver 8004  # Grading Service
   ```

2. Make sure you've created a superuser:
   ```bash
   python manage.py createsuperuser
   ```

## 1. Student Service (Port 8001)

### API Root
Visit: http://localhost:8001/api/
You should see available endpoints:
- students/
- registrations/

### Browse Students
1. Visit: http://localhost:8001/api/students/
2. You can:
   - View all students (GET)
   - Create new student using the HTML form (POST)
   - Filter students using query parameters

### Admin Interface
1. Visit: http://localhost:8001/admin/
2. Login with superuser credentials
3. Manage students and registrations

## 2. Course Service (Port 8002)

### API Root
Visit: http://localhost:8002/api/
Available endpoints:
- courses/
- curricula/
- curriculum-courses/

### Browse Courses
1. Visit: http://localhost:8002/api/courses/
2. You can:
   - View all courses
   - Create new course
   - View prerequisites by clicking on a course

### Browse Curricula
1. Visit: http://localhost:8002/api/curricula/
2. You can:
   - View all curricula
   - Create new curriculum
   - Associate courses with curricula

### Admin Interface
Visit: http://localhost:8002/admin/
Manage:
- Courses
- Curricula
- Curriculum-Course relationships

## 3. Professor Service (Port 8003)

### API Root
Visit: http://localhost:8003/api/
Available endpoints:
- professors/
- assignments/

### Browse Professors
1. Visit: http://localhost:8003/api/professors/
2. You can:
   - View all professors
   - Create new professor
   - View course assignments

### Browse Assignments
Visit: http://localhost:8003/api/assignments/
Manage course assignments for professors

### Admin Interface
Visit: http://localhost:8003/admin/
Manage:
- Professor profiles
- Course assignments

## 4. Grading Service (Port 8004)

### API Root
Visit: http://localhost:8004/api/
Available endpoints:
- grades/
- disputes/

### Browse Grades
1. Visit: http://localhost:8004/api/grades/
2. You can:
   - View all grades
   - Submit new grades
   - Filter grades by student or course

### Browse Grade Disputes
1. Visit: http://localhost:8004/api/disputes/
2. You can:
   - View all disputes
   - Create new dispute
   - Resolve existing disputes

### Admin Interface
Visit: http://localhost:8004/admin/
Manage:
- Grades
- Grade disputes

## Example Workflow

1. Create a Course:
   - Go to http://localhost:8002/api/courses/
   - Fill in the form:
     ```json
     {
         "course_id": "CS101",
         "title": "Introduction to Programming",
         "description": "Basic programming concepts",
         "credits": 3,
         "department": "Computer Science",
         "status": "ACTIVE"
     }
     ```

2. Create a Professor:
   - Go to http://localhost:8003/api/professors/
   - Fill in the form:
     ```json
     {
         "professor_id": "PROF001",
         "first_name": "John",
         "last_name": "Doe",
         "email": "john.doe@university.edu",
         "department": "Computer Science",
         "title": "ASSISTANT",
         "phone_number": "123-456-7890",
         "office_location": "Building A, Room 101"
     }
     ```

3. Create a Student:
   - Go to http://localhost:8001/api/students/
   - Fill in the form:
     ```json
     {
         "student_id": "STU001",
         "first_name": "Jane",
         "last_name": "Smith",
         "email": "jane.smith@university.edu"
     }
     ```

4. Submit a Grade:
   - Go to http://localhost:8004/api/grades/
   - Fill in the form:
     ```json
     {
         "student_id": "STU001",
         "course_id": "CS101",
         "professor_id": "PROF001",
         "grade_value": 95.5,
         "grade_letter": "A",
         "semester": "Fall",
         "year": 2024,
         "comments": "Excellent work"
     }
     ```

## Tips
1. Use the browsable API interface's forms to create and update records
2. Use the "OPTIONS" button to see available fields and their requirements
3. Use the filter buttons to sort and search data
4. Check the "raw data" option to see JSON responses
5. Use the admin interface for more complex operations

## Success Criteria

The system is working correctly if:

1. ✓ Can create courses, professors, and students
2. ✓ Can assign professors to courses
3. ✓ Can submit and retrieve grades
4. ✓ Cross-service validation works
5. ✓ Can view related data across services
6. ✓ Error handling works as expected
7. ✓ Data persistence works


## Common Issues
1. If you get a 404, check if you're using the correct port
2. If you get validation errors, check the required fields
3. Make sure referenced IDs exist in other services before creating relationships
4. Check that all services are running if cross-service validation fails