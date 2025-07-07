from flask import Flask, request, jsonify, Blueprint
from models import db, Category, Week, Submission
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
    """
    data = request.get_json()
    if not data:
        return handle_error("No data provided", 400)

    # Validate required fields
    required_fields = ['student_name', 'project_url']
    if not all(field in data and data[field] for field in required_fields):
        return handle_error("Missing required fields: student_name, project_url", 400)

    try:
        # Find the week for the submission
        week = Week.query.filter_by(category_id=category_id, week_number=week_number).first_or_404()

        # Create a new submission
        submission = Submission(
            student_name=data['student_name'],
            week_id=week.id,
            project_url=data['project_url'],
            comment=data.get('comment'),
            project_type=week.category.name.lower()  # Set project_type from category
        )
        db.session.add(submission)
        db.session.commit()
        
        return jsonify(submission.to_dict()), 201

    except IntegrityError as e:
        db.session.rollback()
        return handle_error(f"Database integrity error: {e}", 400)
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)


# --- Project Submission Routes ---

# GET /project-submissions - List all project submissions
@api.route('/project-submissions', methods=['GET'])
def get_project_submissions():
    """
    Returns a list of all project submissions, ordered by most recent.
    """
    try:
        submissions = ProjectSubmission.query.order_by(ProjectSubmission.submitted_at.desc()).all()
        return jsonify([s.to_dict() for s in submissions])
    except Exception as e:
        return handle_error(e, 500)

# POST /project-submissions - Submit a new project
@api.route('/project-submissions', methods=['POST'])
def submit_new_project():
    """
    Submits a new project with a name and a link.
    
    Example request:
    {
        "name": "Jane Doe",
        "project_link": "https://github.com/janedoe/my-awesome-project"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return handle_error("No data provided", 400)
        
        name = data.get('name')
        project_link = data.get('project_link')
        
        if not name or not project_link:
            return handle_error("Missing 'name' or 'project_link'", 400)
        
        new_submission = ProjectSubmission(
            name=name,
            project_link=project_link
        )
        
        db.session.add(new_submission)
        db.session.commit()
        
        return jsonify(new_submission.to_dict()), 201
        
    except IntegrityError as e:
        db.session.rollback()
        return handle_error(f"Database integrity error: {e}", 400)
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)
