"""Admin API routes for SparkRepo.

Endpoints in this module require JWT auth and admin privileges.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db_service import DatabaseService
from auth import admin_required
from datetime import datetime
from utils.validators import parse_iso8601
from utils.errors import json_error

admin_api = Blueprint('admin_api', __name__)

# Admin - Get all weeks across all classes
@admin_api.route('/weeks', methods=['GET'])
@jwt_required()
@admin_required
def get_all_weeks():
    """
    Admin only - Get all weeks across all classes.
    
    Example response:
    {
        "weeks": [
            {
                "id": 1,
                "category_id": 1,
                "category_name": "Coding for Kids 001 (2025)",
                "week_number": 1,
                "title": "Week 1: Introduction to Scratch",
                "display_name": "Introduction to Scratch",
                "is_active": true
            }
        ]
    }
    """
    db = DatabaseService()
    weeks = db.get_all_weeks()
    result = []
    
    for week in weeks:
        result.append({
            "id": week['id'],
            "category_id": week['category_id'],
            "category_name": week.get('category_name'),
            "week_number": week['week_number'],
            "title": week['title'],
            "display_name": week.get('display_name') or week['title'],
            "is_active": week.get('is_active', True)
        })
    
    return jsonify({"weeks": result}), 200

# Admin - Update week details
@admin_api.route('/weeks/<int:week_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_week(week_id):
    """
    Admin only - Update week details.
    
    Example request:
    {
        "title": "Updated Week Title",
        "display_name": "Custom Display Name",
        "description": "Updated description",
        "assignment_url": "https://scratch.mit.edu/projects/updated",
        "due_date": "2025-06-15T23:59:59",
        "is_active": true
    }
    
    Example response:
    {
        "message": "Week updated successfully",
        "week": {
            "id": 1,
            "category_id": 1,
            "week_number": 1,
            "title": "Updated Week Title",
            "display_name": "Custom Display Name",
            "description": "Updated description",
            "assignment_url": "https://scratch.mit.edu/projects/updated",
            "due_date": "2025-06-15T23:59:59",
            "is_active": true
        }
    }
    """
    db = DatabaseService(use_admin=True)
    week = db.get_week_by_id(week_id)
    
    if not week:
        return json_error("Week not found", 404)
    
    data = request.get_json()
    
    if not data:
        return json_error("No data provided", 400)
    
    # Prepare update data
    update_data = {}
    if 'title' in data:
        update_data['title'] = data['title']
    if 'display_name' in data:
        update_data['display_name'] = data['display_name']
    if 'description' in data:
        update_data['description'] = data['description']
    if 'assignment_url' in data:
        update_data['assignment_url'] = data['assignment_url']
    if 'due_date' in data and data['due_date']:
        try:
            update_data['due_date'] = parse_iso8601(data['due_date'])
        except ValueError:
            return json_error("Invalid date format", 400)
    if 'is_active' in data:
        update_data['is_active'] = data['is_active']
    
    updated_week = db.update_week(week_id, **update_data)
    
    if not updated_week:
        return json_error("Failed to update week", 500)
    
    return jsonify({
        "message": "Week updated successfully",
        "week": updated_week
    }), 200

# Admin - Create a new week
@admin_api.route('/categories/<int:category_id>/weeks', methods=['POST'])
@jwt_required()
@admin_required
def create_week(category_id):
    """
    Admin only - Create a new week for a class.
    
    Example request:
    {
        "week_number": 1,
        "title": "New Week",
        "display_name": "Custom Display Name",
        "description": "Week description",
        "assignment_url": "https://scratch.mit.edu/projects/example",
        "due_date": "2025-06-15T23:59:59"
    }
    
    Example response:
    {
        "message": "Week created successfully",
        "week": {
            "id": 1,
            "category_id": 1,
            "week_number": 1,
            "title": "New Week",
            "display_name": "Custom Display Name",
            "description": "Week description",
            "assignment_url": "https://scratch.mit.edu/projects/example",
            "due_date": "2025-06-15T23:59:59",
            "is_active": true
        }
    }
    """
    db = DatabaseService(use_admin=True)
    
    # Check if category exists
    category = db.get_category(category_id)
    if not category:
        return json_error("Category not found", 404)
    
    data = request.get_json()
    
    if not data or 'week_number' not in data or 'title' not in data:
        return json_error("Missing required fields", 400)
    
    # Check if week number already exists for this category
    if db.check_week_exists(category_id, data['week_number']):
        return json_error("Week number already exists for this category", 400)
    
    # Parse due date if provided
    due_date = None
    if 'due_date' in data and data['due_date']:
        try:
            due_date = parse_iso8601(data['due_date'])
        except ValueError:
            return json_error("Invalid date format", 400)
    
    # Create new week
    new_week = db.create_week(
        category_id=category_id,
        week_number=data['week_number'],
        title=data['title'],
        display_name=data.get('display_name'),
        description=data.get('description'),
        assignment_url=data.get('assignment_url'),
        due_date=due_date,
        is_active=data.get('is_active', True)
    )
    
    if not new_week:
        return json_error("Failed to create week", 500)
    
    return jsonify({
        "message": "Week created successfully",
        "week": new_week
    }), 201

# Admin - Get all submissions
@admin_api.route('/submissions', methods=['GET'])
@jwt_required()
@admin_required
def get_all_submissions():
    """
    Admin only - Get all submissions with optional filters.
    
    Query parameters:
    - category_id: Filter by category ID
    - week_id: Filter by week ID
    - status: Filter by submission status
    
    Example response:
    {
        "submissions": [
            {
                "id": 1,
                "student_name": "John Doe",
                "week_id": 1,
                "week_number": 1,
                "week_title": "Introduction to Scratch",
                "project_url": "https://scratch.mit.edu/projects/123456",
                "comment": "My first Scratch project!",
                "admin_comment": null,
                "status": "submitted",
                "submitted_at": "2025-05-23T14:30:00"
            }
        ]
    }
    """
    db = DatabaseService(use_admin=True)
    
    # Get filter parameters
    category_id = request.args.get('category_id', type=int)
    week_id = request.args.get('week_id', type=int)
    status = request.args.get('status')
    
    # Get submissions with filters
    submissions = db.get_all_submissions(
        category_id=category_id,
        week_id=week_id,
        status=status
    )
    
    return jsonify({
        "submissions": submissions
    }), 200

# Admin - Update submission status
@admin_api.route('/submissions/<int:submission_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_submission(submission_id):
    """
    Admin only - Update submission status and add admin comments.
    
    Example request:
    {
        "status": "approved",
        "admin_comment": "Great job on this project!"
    }
    
    Example response:
    {
        "message": "Submission updated successfully",
        "submission": {
            "id": 1,
            "student_name": "John Doe",
            "week_id": 1,
            "week_number": 1,
            "week_title": "Introduction to Scratch",
            "project_url": "https://scratch.mit.edu/projects/123456",
            "comment": "My first Scratch project!",
            "admin_comment": "Great job on this project!",
            "status": "approved",
            "submitted_at": "2025-05-23T14:30:00",
            "last_modified": "2025-05-25T10:15:00"
        }
    }
    """
    db = DatabaseService(use_admin=True)
    submission = db.get_submission(submission_id)
    
    if not submission:
        return json_error("Submission not found", 404)
    
    data = request.get_json()
    
    if not data:
        return json_error("No data provided", 400)
    
    # Get current admin user
    current_user_id = get_jwt_identity()
    
    # Prepare update data
    update_data = {}
    if 'status' in data:
        update_data['status'] = data['status']
    
    if 'admin_comment' in data:
        update_data['admin_comment'] = data['admin_comment']
    
    # Track who modified it
    update_data['modified_by'] = current_user_id
    
    updated_submission = db.update_submission(submission_id, **update_data)
    
    if not updated_submission:
        return json_error("Failed to update submission", 500)
    
    return jsonify({
        "message": "Submission updated successfully",
        "submission": updated_submission
    }), 200

# Admin - Delete submission
@admin_api.route('/submissions/<int:submission_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_submission(submission_id):
    """
    Admin only - Delete a submission.
    
    Example response:
    {
        "message": "Submission deleted successfully"
    }
    """
    db = DatabaseService(use_admin=True)
    submission = db.get_submission(submission_id)
    
    if not submission:
        return json_error("Submission not found", 404)
    
    db.delete_submission(submission_id)
    
    return jsonify({
        "message": "Submission deleted successfully"
    }), 200
