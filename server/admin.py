"""Admin endpoints for managing weeks and submissions with Firebase."""
from flask import Blueprint, request, jsonify
from .models import Week, Submission, Category
from .auth import admin_required
import logging

logger = logging.getLogger(__name__)

admin_api = Blueprint('admin_api', __name__)


# Admin - Get all weeks across all categories
@admin_api.route('/weeks', methods=['GET'])
@admin_required
def get_all_weeks():
    """
    Admin only - Get all weeks across all categories.
    
    Example response:
    {
        "weeks": [
            {
                "id": "week123",
                "category_id": "cat123",
                "week_number": 1,
                "title": "Week 1: Introduction to Scratch",
                "is_active": true
            }
        ]
    }
    """
    try:
        weeks = Week.get_all()
        
        # Enrich with category names
        result = []
        for week in weeks:
            category = Category.get_by_id(week['category_id'])
            week_data = {**week}
            week_data['category_name'] = category['name'] if category else 'Unknown'
            result.append(week_data)
        
        return jsonify({"weeks": result}), 200
    except Exception as e:
        logger.error(f"Get all weeks error: {e}")
        return jsonify({"error": str(e)}), 500


# Admin - Update week details
@admin_api.route('/weeks/<string:week_id>', methods=['PUT'])
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
        "category_id": "new_category_id",
        "is_active": true
    }
    """
    try:
        week = Week.get_by_id(week_id)
        if not week:
            return jsonify({"error": "Week not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Update week with provided fields
        updated_week = Week.update(
            week_id,
            title=data.get('title'),
            category_id=data.get('category_id'),
            display_name=data.get('display_name'),
            description=data.get('description'),
            assignment_url=data.get('assignment_url'),
            due_date=data.get('due_date'),
            is_active=data.get('is_active')
        )
        
        logger.info(f"Week updated: {week_id}")
        
        return jsonify({
            "message": "Week updated successfully",
            "week": updated_week
        }), 200
        
    except Exception as e:
        logger.error(f"Update week error: {e}")
        return jsonify({"error": str(e)}), 500


# Admin - Create new week for a category
@admin_api.route('/categories/<string:category_id>/weeks', methods=['POST'])
@admin_required
def create_week(category_id):
    """
    Admin only - Create a new week for a category.
    
    Example request:
    {
        "week_number": 2,
        "title": "Week 2: Variables",
        "display_name": "Variables",
        "description": "Learn about variables in Scratch",
        "assignment_url": "https://scratch.mit.edu/projects/123",
        "due_date": "2025-06-22T23:59:59",
        "is_active": true
    }
    """
    try:
        category = Category.get_by_id(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404
        
        data = request.get_json()
        if not data or 'week_number' not in data or 'title' not in data:
            return jsonify({"error": "Missing required fields: week_number and title"}), 400
        
        # Check if week already exists
        existing = Week.get_by_category_and_number(category_id, data['week_number'])
        if existing:
            return jsonify({"error": "Week number already exists for this category"}), 400
        
        # Create new week
        week = Week.create(
            category_id=category_id,
            week_number=data['week_number'],
            title=data['title'],
            display_name=data.get('display_name'),
            description=data.get('description'),
            assignment_url=data.get('assignment_url'),
            due_date=data.get('due_date'),
            is_active=data.get('is_active', True)
        )
        
        logger.info(f"Week created: {week['id']} for category {category_id}")
        
        return jsonify({
            "message": "Week created successfully",
            "week": week
        }), 201
        
    except Exception as e:
        logger.error(f"Create week error: {e}")
        return jsonify({"error": str(e)}), 500


# Admin - Delete week
@admin_api.route('/weeks/<string:week_id>', methods=['DELETE'])
@admin_required
def delete_week(week_id):
    """Admin only - Delete a week and all its submissions."""
    try:
        week = Week.get_by_id(week_id)
        if not week:
            return jsonify({"error": "Week not found"}), 404
        
        Week.delete(week_id)
        
        logger.info(f"Week deleted: {week_id}")
        
        return jsonify({"message": "Week deleted successfully"}), 200
        
    except Exception as e:
        logger.error(f"Delete week error: {e}")
        return jsonify({"error": str(e)}), 500


# Admin - Get all submissions
@admin_api.route('/submissions', methods=['GET'])
@admin_required
def get_all_submissions():
    """
    Admin only - Get all submissions with optional filters.
    
    Query params:
    - week_id: Filter by week
    - status: Filter by status (pending, reviewed, approved)
    """
    try:
        week_id = request.args.get('week_id')
        status = request.args.get('status')
        class_id = request.args.get('class_id')
        
        if week_id:
            submissions = Submission.get_by_week(week_id)
        else:
            submissions = Submission.get_all()

        # Filter by class/category if provided.
        # Submissions only store week_id, so we join against weeks to determine category_id.
        if class_id:
            weeks = Week.get_all()
            week_ids_for_class = {w.get('id') for w in weeks if w.get('category_id') == class_id}
            submissions = [s for s in submissions if s.get('week_id') in week_ids_for_class]
        
        # Filter by status if provided
        if status:
            submissions = [s for s in submissions if s.get('status') == status]

        # Ensure consistent ordering (newest first)
        try:
            submissions.sort(key=lambda s: s.get('submitted_at'), reverse=True)
        except Exception:
            pass
        
        return jsonify({"submissions": submissions}), 200
        
    except Exception as e:
        logger.error(f"Get all submissions error: {e}")
        return jsonify({"error": str(e)}), 500


# Admin - Update submission
@admin_api.route('/submissions/<string:submission_id>', methods=['PUT'])
@admin_required
def update_submission(submission_id):
    """
    Admin only - Update a submission (status, comment).
    
    Example request:
    {
        "status": "reviewed",
        "admin_comment": "Great work!"
    }
    """
    try:
        from flask_jwt_extended import get_jwt_identity
        
        submission = Submission.get_by_id(submission_id)
        if not submission:
            return jsonify({"error": "Submission not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        current_user_id = get_jwt_identity()
        
        # Update submission
        updated_submission = Submission.update(
            submission_id,
            status=data.get('status'),
            admin_comment=data.get('admin_comment'),
            modified_by=current_user_id
        )
        
        logger.info(f"Submission updated: {submission_id}")
        
        return jsonify({
            "message": "Submission updated successfully",
            "submission": updated_submission
        }), 200
        
    except Exception as e:
        logger.error(f"Update submission error: {e}")
        return jsonify({"error": str(e)}), 500


# Admin - Delete submission
@admin_api.route('/submissions/<string:submission_id>', methods=['DELETE'])
@admin_required
def delete_submission(submission_id):
    """Admin only - Delete a submission."""
    try:
        submission = Submission.get_by_id(submission_id)
        if not submission:
            return jsonify({"error": "Submission not found"}), 404
        
        Submission.delete(submission_id)
        
        logger.info(f"Submission deleted: {submission_id}")
        
        return jsonify({"message": "Submission deleted successfully"}), 200
        
    except Exception as e:
        logger.error(f"Delete submission error: {e}")
        return jsonify({"error": str(e)}), 500


# Admin - Create category
@admin_api.route('/categories', methods=['POST'])
@admin_required
def create_category():
    """
    Admin only - Create a new category.
    
    Example request:
    {
        "name": "Canva Design",
        "description": "Learn graphic design with Canva"
    }
    """
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({"error": "Missing required field: name"}), 400
        
        category = Category.create(
            name=data['name'],
            description=data.get('description')
        )
        
        logger.info(f"Category created: {category['id']}")
        
        return jsonify({
            "message": "Category created successfully",
            "category": category
        }), 201
        
    except Exception as e:
        logger.error(f"Create category error: {e}")
        return jsonify({"error": str(e)}), 500


# Admin - Update category
@admin_api.route('/categories/<string:category_id>', methods=['PUT'])
@admin_required
def update_category(category_id):
    """Admin only - Update a category."""
    try:
        category = Category.get_by_id(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        updated_category = Category.update(
            category_id,
            name=data.get('name'),
            description=data.get('description')
        )
        
        logger.info(f"Category updated: {category_id}")
        
        return jsonify({
            "message": "Category updated successfully",
            "category": updated_category
        }), 200
        
    except Exception as e:
        logger.error(f"Update category error: {e}")
        return jsonify({"error": str(e)}), 500


# Admin - Delete category
@admin_api.route('/categories/<string:category_id>', methods=['DELETE'])
@admin_required
def delete_category(category_id):
    """Admin only - Delete a category and all its weeks."""
    try:
        category = Category.get_by_id(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404
        
        Category.delete(category_id)
        
        logger.info(f"Category deleted: {category_id}")
        
        return jsonify({"message": "Category deleted successfully"}), 200
        
    except Exception as e:
        logger.error(f"Delete category error: {e}")
        return jsonify({"error": str(e)}), 500
