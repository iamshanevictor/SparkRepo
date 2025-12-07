"""Public API routes for SparkRepo.

Provides category, week, and submission endpoints used by the student UI.
"""
from flask import request, jsonify, Blueprint
from db_service import DatabaseService
from utils.errors import json_error, handle_exception
from utils.validators import (
    validate_required_fields,
    validate_url,
    validate_fields_strict,
    sanitize_string,
    parse_iso8601
)
from utils.exceptions import NotFoundError, ValidationError
import logging

logger = logging.getLogger(__name__)

# Create a Blueprint for API routes
api = Blueprint('api', __name__)

def _get_week_or_404(category_id: int, week_number: int, db: DatabaseService):
    """Get a week or raise NotFoundError."""
    category = db.get_category(category_id)
    if not category:
        raise NotFoundError("Category")
    
    week = db.get_week(category_id, week_number)
    if not week:
        raise NotFoundError("Week")
    
    return week

# GET /categories - List all categories
@api.route('/categories', methods=['GET'])
def get_categories():
    """
    Returns a list of all available categories.
    """
    try:
        db = DatabaseService()
        categories = db.get_all_categories()
        return jsonify(categories)
    except Exception as e:
        return handle_exception(e, 500)

# GET /categories/{id} - Get a specific category
@api.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Returns details for a specific category.
    """
    try:
        db = DatabaseService()
        category = db.get_category(category_id)
        if not category:
            return json_error("Category not found", 404)
        return jsonify(category)
    except Exception as e:
        return handle_exception(e, 500)

# GET /categories/{id}/weeks - List all weeks for a category
@api.route('/categories/<int:category_id>/weeks', methods=['GET'])
def get_category_weeks(category_id):
    """
    Returns all weeks for a specific category.
    """
    try:
        db = DatabaseService()
        category = db.get_category(category_id)
        if not category:
            return json_error("Category not found", 404)
        weeks = db.get_weeks_by_category(category_id)
        return jsonify(weeks)
    except Exception as e:
        return handle_exception(e, 500)

# GET /categories/{id}/weeks/{week} - Get a specific week's assignment
@api.route('/categories/<int:category_id>/weeks/<int:week_number>', methods=['GET'])
def get_week_assignment(category_id, week_number):
    """
    Returns details for a specific week's assignment.
    
    Example response:
    {
        "id": 1,
        "category_id": 1,
        "week_number": 1,
        "title": "Introduction to Scratch",
        "description": "Learn the basics of Scratch programming",
        "assignment_url": "https://scratch.mit.edu/projects/example",
        "due_date": "2025-06-01T23:59:59",
        "submissions": [
            {
                "id": 1,
                "student_name": "John Doe",
                "project_url": "https://scratch.mit.edu/projects/123456",
                "submitted_at": "2025-05-28T14:30:00"
            }
        ]
    }
    """
    try:
        db = DatabaseService()
        week = _get_week_or_404(category_id, week_number, db)
        
        # Add submissions data if requested (can be controlled by query param)
        include_submissions = request.args.get('include_submissions', 'false').lower() == 'true'
        if include_submissions:
            submissions = db.get_submissions_by_week(week['id'])
            week['submissions'] = submissions
        
        return jsonify(week)
    except Exception as e:
        return handle_exception(e, 500)

# POST /categories/{id}/weeks/{week}/submissions - Submit a project link
@api.route('/categories/<int:category_id>/weeks/<int:week_number>/submissions', methods=['POST'])
def submit_project(category_id, week_number):
    """Submit a project link for a specific week."""
    try:
        data = request.get_json()
        if not data:
            raise ValidationError("No JSON data provided")

        # Validate required fields
        try:
            validate_fields_strict(data, ['student_name', 'project_url'])
        except ValidationError as e:
            return json_error(str(e), 400)
        
        # Validate and sanitize inputs
        student_name = sanitize_string(data['student_name'], max_length=100)
        if not student_name:
            raise ValidationError("Student name cannot be empty")
        
        project_url = data['project_url'].strip()
        if not validate_url(project_url):
            raise ValidationError("Invalid project URL format")
        
        # Optional comment
        comment = None
        if 'comment' in data and data['comment']:
            comment = sanitize_string(data['comment'], max_length=500)
        
        db = DatabaseService()
        # Find the week for the submission
        week = _get_week_or_404(category_id, week_number, db)
        
        # Get category to determine project type
        category = db.get_category(category_id)
        project_type = category['name'].lower() if category else 'scratch'

        # Create a new submission
        submission = db.create_submission(
            student_name=student_name,
            week_id=week['id'],
            project_url=project_url,
            comment=comment,
            project_type=project_type
        )
        
        if not submission:
            raise ValidationError("Failed to create submission")
        
        logger.info(f"Submission created: student={student_name}, week={week_number}, category={category_id}")
        return jsonify(submission), 201

    except NotFoundError as e:
        return json_error(str(e), 404)
    except ValidationError as e:
        return json_error(str(e), 400)
    except Exception as e:
        return handle_exception(e, 500)

