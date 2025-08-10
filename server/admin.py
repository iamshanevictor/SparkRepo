"""Admin endpoints for managing weeks and submissions.

All routes require a valid JWT and admin privileges. This module centralizes
date parsing via utils.datetime.parse_iso_datetime to ensure consistent
handling of ISO strings coming from the client.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Week, Submission, Category, Student, User
from auth import admin_required
from datetime import datetime
from utils.datetime import parse_iso_datetime

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
                "class_id": 1,
                "class_name": "Coding for Kids 001 (2025)",
                "week_number": 1,
                "title": "Week 1: Introduction to Scratch",
                "display_name": "Introduction to Scratch",
                "is_active": true
            }
        ]
    }
    """
    weeks = Week.query.all()
    result = []
    
    for week in weeks:
        result.append({
            "id": week.id,
            "category_id": week.category_id,
            "category_name": week.category.name,
            "week_number": week.week_number,
            "title": week.title,
            "display_name": week.display_name or week.title,
            "is_active": week.is_active
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
            "class_id": 1,
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
    week = Week.query.get_or_404(week_id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Update fields if provided
    if 'title' in data:
        week.title = data['title']
    if 'display_name' in data:
        week.display_name = data['display_name']
    if 'description' in data:
        week.description = data['description']
    if 'assignment_url' in data:
        week.assignment_url = data['assignment_url']
    if 'due_date' in data and data['due_date']:
        try:
            week.due_date = parse_iso_datetime(data['due_date'])
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400
    if 'is_active' in data:
        week.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify({
        "message": "Week updated successfully",
        "week": week.to_dict()
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
            "class_id": 1,
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
    # Check if category exists
    category = Category.query.get_or_404(category_id)
    
    data = request.get_json()
    
    if not data or 'week_number' not in data or 'title' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    # Check if week number already exists for this category
    existing_week = Week.query.filter_by(
        category_id=category_id, 
        week_number=data['week_number']
    ).first()
    
    if existing_week:
        return jsonify({"error": "Week number already exists for this category"}), 400
    
    # Create new week
    new_week = Week(
        category_id=category_id,
        week_number=data['week_number'],
        title=data['title'],
        display_name=data.get('display_name'),
        description=data.get('description'),
        assignment_url=data.get('assignment_url'),
        is_active=data.get('is_active', True)
    )
    
    # Set due date if provided
    if 'due_date' in data and data['due_date']:
        try:
            new_week.due_date = parse_iso_datetime(data['due_date'])
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400
    
    db.session.add(new_week)
    db.session.commit()
    
    return jsonify({
        "message": "Week created successfully",
        "week": new_week.to_dict()
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
                "student_id": 1,
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
    # Get filter parameters
    category_id = request.args.get('category_id', type=int)
    week_id = request.args.get('week_id', type=int)
    status = request.args.get('status')
    
    # Start with base query
    query = Submission.query
    
    # Apply filters if provided
    if category_id:
        # Join with Week to filter by class_id
        query = query.join(Week).filter(Week.category_id == category_id)
    
    if week_id:
        query = query.filter(Submission.week_id == week_id)
    
    if status:
        query = query.filter(Submission.status == status)
    
    # Get results
    submissions = query.all()
    
    return jsonify({
        "submissions": [sub.to_dict() for sub in submissions]
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
            "student_id": 1,
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
    submission = Submission.query.get_or_404(submission_id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Get current admin user
    current_user_id = get_jwt_identity()
    
    # Update fields if provided
    if 'status' in data:
        submission.status = data['status']
    
    if 'admin_comment' in data:
        submission.admin_comment = data['admin_comment']
    
    # Track who modified it
    submission.modified_by = current_user_id
    
    db.session.commit()
    
    return jsonify({
        "message": "Submission updated successfully",
        "submission": submission.to_dict()
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
    submission = Submission.query.get_or_404(submission_id)
    
    db.session.delete(submission)
    db.session.commit()
    
    return jsonify({
        "message": "Submission deleted successfully"
    }), 200
