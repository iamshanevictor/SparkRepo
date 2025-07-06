from flask import Flask, request, jsonify, Blueprint
from models import db, Category, Week, Student, Submission
from datetime import datetime
from sqlalchemy.exc import IntegrityError

# Create a Blueprint for API routes
api = Blueprint('api', __name__)

# Error handling
def handle_error(e, status_code=400):
    return jsonify({'error': str(e)}), status_code

# GET /categories - List all categories
@api.route('/categories', methods=['GET'])
def get_categories():
    """
    Returns a list of all available categories.
    """
    try:
        categories = Category.query.all()
        return jsonify([category.to_dict() for category in categories])
    except Exception as e:
        return handle_error(e, 500)

# GET /categories/{id} - Get a specific category
@api.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Returns details for a specific category.
    """
    try:
        category = Category.query.get_or_404(category_id)
        return jsonify(category.to_dict())
    except Exception as e:
        return handle_error(e, 500)

# GET /categories/{id}/weeks - List all weeks for a category
@api.route('/categories/<int:category_id>/weeks', methods=['GET'])
def get_category_weeks(category_id):
    """
    Returns all weeks for a specific category.
    """
    try:
        Category.query.get_or_404(category_id)  # Check if category exists
        weeks = Week.query.filter_by(category_id=category_id).order_by(Week.week_number).all()
        return jsonify([week.to_dict() for week in weeks])
    except Exception as e:
        return handle_error(e, 500)

# GET /categories/{id}/weeks/{week} - Get a specific week's assignment
@api.route('/categories/<int:category_id>/weeks/<int:week_number>', methods=['GET'])
def get_week_assignment(category_id, week_number):
    """
    Returns details for a specific week's assignment.
    
    Example response:
    {
        "id": 1,
        "class_id": 1,
        "week_number": 1,
        "title": "Introduction to Scratch",
        "description": "Learn the basics of Scratch programming",
        "assignment_url": "https://scratch.mit.edu/projects/example",
        "due_date": "2025-06-01T23:59:59",
        "submissions": [
            {
                "id": 1,
                "student_id": 1,
                "student_name": "John Doe",
                "project_url": "https://scratch.mit.edu/projects/123456",
                "submitted_at": "2025-05-28T14:30:00"
            }
        ]
    }
    """
    try:
        Category.query.get_or_404(category_id)  # Check if category exists
        week = Week.query.filter_by(category_id=category_id, week_number=week_number).first_or_404()
        
        # Get the week data
        week_data = week.to_dict()
        
        # Add submissions data if requested (can be controlled by query param)
        include_submissions = request.args.get('include_submissions', 'false').lower() == 'true'
        if include_submissions:
            submissions = Submission.query.filter_by(week_id=week.id).all()
            week_data['submissions'] = [sub.to_dict() for sub in submissions]
        
        return jsonify(week_data)
    except Exception as e:
        return handle_error(e, 500)

# POST /categories/{id}/weeks/{week}/submissions - Submit a project link
@api.route('/categories/<int:category_id>/weeks/<int:week_number>/submissions', methods=['POST'])
def submit_project(category_id, week_number):
    """
    Submit a project link for a specific week.
    
    Example request:
    {
        "student_id": 1,
        "project_url": "https://scratch.mit.edu/projects/123456",
        "comment": "This is my first Scratch project!"
    }
    
    Example response:
    {
        "id": 1,
        "student_id": 1,
        "student_name": "John Doe",
        "week_id": 1,
        "week_number": 1,
        "project_url": "https://scratch.mit.edu/projects/123456",
        "comment": "This is my first Scratch project!",
        "submitted_at": "2025-05-28T14:30:00"
    }
    """
    try:
        # Validate request data
        data = request.get_json()
        if not data:
            return handle_error("No data provided", 400)
        
        required_fields = ['student_id', 'project_url']
        for field in required_fields:
            if field not in data:
                return handle_error(f"Missing required field: {field}", 400)

        project_type = data.get('project_type', 'scratch')
        project_url = data['project_url']

        # Validate URL format based on project type
        if project_type == 'scratch' and not project_url.startswith('https://scratch.mit.edu/projects/'):
            return handle_error("Invalid Scratch project URL", 400)
        elif project_type == 'canva' and not project_url.startswith('https://www.canva.com/design/'):
            return handle_error("Invalid Canva project URL", 400)
        elif project_type not in ['scratch', 'canva']:
            return handle_error("Invalid project type specified", 400)
        
        # Get the week
        week = Week.query.filter_by(category_id=category_id, week_number=week_number).first_or_404()
        
        # Check if student exists
        student = Student.query.get_or_404(data['student_id'])
        
        # Check if submission already exists
        existing_submission = Submission.query.filter_by(
            student_id=student.id, 
            week_id=week.id
        ).first()
        
        if existing_submission:
            # Update existing submission
            existing_submission.project_type = data.get('project_type', 'scratch')
            existing_submission.project_url = data['project_url']
            existing_submission.comment = data.get('comment')
            existing_submission.last_modified = datetime.utcnow()
            db.session.commit()
            return jsonify(existing_submission.to_dict())
        else:
            # Create new submission
            submission = Submission(
                student_id=student.id,
                week_id=week.id,
                project_type=data.get('project_type', 'scratch'),
                project_url=data['project_url'],
                comment=data.get('comment')
            )
            db.session.add(submission)
            db.session.commit()
            return jsonify(submission.to_dict()), 201
            
    except IntegrityError:
        db.session.rollback()
        return handle_error("Database integrity error. Submission may already exist.", 400)
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 500)

# Additional routes for student management

# GET /students - List all students
@api.route('/students', methods=['GET'])
def get_students():
    """
    Returns a list of all students.
    
    Example response:
    [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com"
        }
    ]
    """
    try:
        students = Student.query.all()
        return jsonify([student.to_dict() for student in students])
    except Exception as e:
        return handle_error(e, 500)

# GET /students/{id}/submissions - Get all submissions for a student
@api.route('/students/<int:student_id>/submissions', methods=['GET'])
def get_student_submissions(student_id):
    """
    Returns all submissions for a specific student.
    
    Example response:
    [
        {
            "id": 1,
            "student_id": 1,
            "student_name": "John Doe",
            "week_id": 1,
            "week_number": 1,
            "project_url": "https://scratch.mit.edu/projects/123456",
            "comment": "This is my first Scratch project!",
            "submitted_at": "2025-05-28T14:30:00"
        }
    ]
    """
    try:
        Student.query.get_or_404(student_id)  # Check if student exists
        submissions = Submission.query.filter_by(student_id=student_id).all()
        return jsonify([sub.to_dict() for sub in submissions])
    except Exception as e:
        return handle_error(e, 500)
