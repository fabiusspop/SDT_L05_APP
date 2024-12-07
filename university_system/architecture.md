# University System Architecture

## System Overview

The university system is composed of four microservices that communicate via REST APIs:

[Student Service :8001] --- [Course Service :8002]
[Professor Service :8003] --- [Course Service :8002]
[Grading Service :8004] --- [Student Service :8001]
[Grading Service :8004] --- [Professor Service :8003]
[Grading Service :8004] --- [Course Service :8002]

## Service Architecture

### 1. Student Service (Port 8001)
Primary Database Tables:
- Students
- Registrations

API Endpoints:
GET    /api/students/                  # List all students
POST   /api/students/                  # Create new student
GET    /api/students/{student_id}/     # Get student details
PUT    /api/students/{student_id}/     # Update student
DELETE /api/students/{student_id}/     # Delete student
GET    /api/registrations/             # List registrations
POST   /api/registrations/             # Create registration

Interactions:
- Called by: Grading Service (for grade validation)
- Calls to: Course Service (for registration validation)

### 2. Professor Service (Port 8003)
Primary Database Tables:
- Professors
- CourseAssignments

API Endpoints:
GET    /api/professors/                    # List professors
POST   /api/professors/                    # Create professor
GET    /api/professors/{professor_id}/     # Get professor details
PUT    /api/professors/{professor_id}/     # Update professor
DELETE /api/professors/{professor_id}/     # Delete professor
GET    /api/assignments/                   # List assignments
POST   /api/assignments/                   # Create assignment
GET    /api/professors/{id}/assignments/   # Get professor assignments

Interactions:
- Called by: Grading Service (for grade validation)
- Calls to: Course Service (for assignment validation)

### 3. Course Service (Port 8002)
Primary Database Tables:
- Courses
- Curricula
- CurriculumCourses

API Endpoints:
GET    /api/courses/                   # List courses
POST   /api/courses/                   # Create course
GET    /api/courses/{course_id}/       # Get course details
PUT    /api/courses/{course_id}/       # Update course
DELETE /api/courses/{course_id}/       # Delete course
GET    /api/curricula/                 # List curricula
POST   /api/curricula/                 # Create curriculum
GET    /api/curriculum-courses/        # List curriculum courses
GET    /api/courses/{id}/prerequisites/# Get course prerequisites

Interactions:
- Called by: 
  - Student Service (for registration validation)
  - Professor Service (for assignment validation)
  - Grading Service (for grade validation)

### 4. Grading Service (Port 8004)
Primary Database Tables:
- Grades
- GradeDisputes

API Endpoints:
GET    /api/grades/                    # List grades
POST   /api/grades/                    # Submit grade
GET    /api/grades/student_grades/     # Get student grades
GET    /api/grades/course_grades/      # Get course grades
GET    /api/disputes/                  # List disputes
POST   /api/disputes/                  # Create dispute
POST   /api/disputes/{id}/resolve/     # Resolve dispute

Interactions:
- Calls to:
  - Student Service (validate student)
  - Professor Service (validate professor)
  - Course Service (validate course)

## Inter-Service Communication

Example: Grade Submission Flow
GradingService -> StudentService: Validate student_id
StudentService --> GradingService: Student validation response
GradingService -> ProfessorService: Validate professor_id
ProfessorService --> GradingService: Professor validation response
GradingService -> CourseService: Validate course_id
CourseService --> GradingService: Course validation response
GradingService -> GradingService: Save grade if all validations pass

## Database Schema

### Student Service Database
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    student_id VARCHAR(20) UNIQUE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(254) UNIQUE
);

CREATE TABLE registrations (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    course_id VARCHAR(20),
    semester VARCHAR(20),
    year INTEGER
);

### Professor Service Database
CREATE TABLE professors (
    id INTEGER PRIMARY KEY,
    professor_id VARCHAR(20) UNIQUE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(254) UNIQUE,
    department VARCHAR(100),
    title VARCHAR(50)
);

CREATE TABLE course_assignments (
    id INTEGER PRIMARY KEY,
    professor_id INTEGER,
    course_id VARCHAR(20),
    semester VARCHAR(20),
    year INTEGER,
    status VARCHAR(20)
);

### Course Service Database
CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    course_id VARCHAR(20) UNIQUE,
    title VARCHAR(200),
    description TEXT,
    credits INTEGER,
    department VARCHAR(100),
    status VARCHAR(20)
);

CREATE TABLE curricula (
    id INTEGER PRIMARY KEY,
    name VARCHAR(200),
    description TEXT,
    department VARCHAR(100),
    status VARCHAR(20)
);

CREATE TABLE curriculum_courses (
    id INTEGER PRIMARY KEY,
    curriculum_id INTEGER,
    course_id INTEGER,
    semester INTEGER,
    is_required BOOLEAN
);

### Grading Service Database
CREATE TABLE grades (
    id INTEGER PRIMARY KEY,
    student_id VARCHAR(20),
    course_id VARCHAR(20),
    professor_id VARCHAR(20),
    grade_value DECIMAL(4,2),
    grade_letter VARCHAR(2),
    semester VARCHAR(20),
    year INTEGER,
    status VARCHAR(20)
);

CREATE TABLE grade_disputes (
    id INTEGER PRIMARY KEY,
    grade_id INTEGER,
    reason TEXT,
    submitted_by VARCHAR(20),
    status VARCHAR(20),
    resolution TEXT
);

## Error Handling

Each service implements standard HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

Example error response:
{
    "error": "Validation Error",
    "detail": "Student ID does not exist",
    "status": 400
}

## Service Dependencies

GradingService -> StudentService
GradingService -> ProfessorService
GradingService -> CourseService
StudentService -> CourseService
ProfessorService -> CourseService

## Key Design Decisions

1. Each service has its own database for independence
2. REST APIs for synchronous communication
3. Cross-service validation for data integrity
4. Standardized error handling across services
5. Modular design for scalability
6. Clear service boundaries and responsibilities

## Deployment Considerations

1. Each service runs on a different port
2. Independent deployment possible
3. Database migrations handled per service
4. Cross-service communication via HTTP
5. Error handling for service unavailability
6. Data consistency across services

## Testing Strategy

1. Unit tests per service
2. Integration tests for cross-service communication
3. End-to-end testing scenarios
4. API contract testing
5. Error handling verification
6. Data validation testing