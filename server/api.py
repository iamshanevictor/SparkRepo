"""Public API blueprint for SparkRepo with Firebase Firestore."""
from flask import request, jsonify, Blueprint
from .models import Category, Week, Submission
import logging

logger = logging.getLogger(__name__)

# Create a Blueprint for API routes
api = Blueprint('api', __name__)


# Error handling
def handle_error(e, status_code=400):
    logger.error(f"API error: {e}")
    return jsonify({'error': str(e)}), status_code


# GET /categories - List all categories
@api.route('/categories', methods=['GET'])
def get_categories():
    """Returns a list of all available categories."""
    try:
        categories = Category.get_all()
        return jsonify({'categories': categories}), 200
    except Exception as e:
        return handle_error(e, 500)


# GET /categories/{id} - Get a specific category
@api.route('/categories/<string:category_id>', methods=['GET'])
def get_category(category_id):
    """Returns details for a specific category."""
    try:
        category = Category.get_by_id(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        return jsonify(category), 200
    except Exception as e:
        return handle_error(e, 500)


# GET /categories/{id}/weeks - List all weeks for a category
@api.route('/categories/<string:category_id>/weeks', methods=['GET'])
def get_category_weeks(category_id):
    """Returns all weeks for a specific category."""
    try:
        category = Category.get_by_id(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        weeks = Week.get_by_category(category_id)
        return jsonify({'weeks': weeks}), 200
    except Exception as e:
        return handle_error(e, 500)


# GET /categories/{id}/weeks/{week} - Get a specific week's assignment
@api.route('/categories/<string:category_id>/weeks/<int:week_number>', methods=['GET'])
def get_week_assignment(category_id, week_number):
    """Returns details for a specific week's assignment."""
    try:
        week = Week.get_by_category_and_number(category_id, week_number)
        if not week:
            return jsonify({'error': 'Week not found'}), 404
        return jsonify(week), 200
    except Exception as e:
        return handle_error(e, 500)


# GET /weeks/{id} - Get week by ID
@api.route('/weeks/<string:week_id>', methods=['GET'])
def get_week(week_id):
    """Returns details for a specific week by ID."""
    try:
        week = Week.get_by_id(week_id)
        if not week:
            return jsonify({'error': 'Week not found'}), 404
        return jsonify(week), 200
    except Exception as e:
        return handle_error(e, 500)


# GET /weeks/{id}/submissions - Get all submissions for a week
@api.route('/weeks/<string:week_id>/submissions', methods=['GET'])
def get_week_submissions(week_id):
    """Returns all submissions for a specific week."""
    try:
        week = Week.get_by_id(week_id)
        if not week:
            return jsonify({'error': 'Week not found'}), 404
        
        submissions = Submission.get_by_week(week_id)
        return jsonify({'submissions': submissions}), 200
    except Exception as e:
        return handle_error(e, 500)


# POST /weeks/{id}/submissions - Create a new submission
@api.route('/weeks/<string:week_id>/submissions', methods=['POST'])
def create_submission(week_id):
    """Create a new submission for a week."""
    try:
        # Verify week exists
        week = Week.get_by_id(week_id)
        if not week:
            return jsonify({'error': 'Week not found'}), 404
        
        # Get submission data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        student_name = data.get('student_name')
        project_url = data.get('project_url')
        
        if not student_name or not project_url:
            return jsonify({'error': 'student_name and project_url are required'}), 400
        
        # Create submission
        submission = Submission.create(
            week_id=week_id,
            student_name=student_name,
            project_url=project_url,
            status='pending'
        )
        
        logger.info(f"Submission created: {submission['id']} for week {week_id}")
        return jsonify({
            'message': 'Submission created successfully',
            'submission': submission
        }), 201
        
    except Exception as e:
        return handle_error(e, 500)


# GET /submissions/{id} - Get a specific submission
@api.route('/submissions/<string:submission_id>', methods=['GET'])
def get_submission(submission_id):
    """Returns details for a specific submission."""
    try:
        submission = Submission.get_by_id(submission_id)
        if not submission:
            return jsonify({'error': 'Submission not found'}), 404
        return jsonify(submission), 200
    except Exception as e:
        return handle_error(e, 500)
