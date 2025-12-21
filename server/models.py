"""Firestore data models and helper functions for SparkRepo."""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .firebase_client import get_firestore_client

# Collection names
CATEGORIES_COLLECTION = 'categories'
USERS_COLLECTION = 'users'
WEEKS_COLLECTION = 'weeks'
SUBMISSIONS_COLLECTION = 'submissions'


class Category:
    """Category model representing a project type, e.g., Scratch or Canva."""
    
    @staticmethod
    def create(name, description=None):
        """Create a new category."""
        db = get_firestore_client()
        category_data = {
            'name': name,
            'description': description,
            'created_at': datetime.utcnow()
        }
        doc_ref = db.collection(CATEGORIES_COLLECTION).document()
        doc_ref.set(category_data)
        return {'id': doc_ref.id, **category_data}
    
    @staticmethod
    def get_all():
        """Get all categories."""
        db = get_firestore_client()
        categories = []
        docs = db.collection(CATEGORIES_COLLECTION).order_by('name').stream()
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            categories.append(data)
        return categories
    
    @staticmethod
    def get_by_id(category_id):
        """Get category by ID."""
        db = get_firestore_client()
        doc = db.collection(CATEGORIES_COLLECTION).document(category_id).get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None
    
    @staticmethod
    def update(category_id, name=None, description=None):
        """Update a category."""
        db = get_firestore_client()
        doc_ref = db.collection(CATEGORIES_COLLECTION).document(category_id)
        update_data = {}
        if name is not None:
            update_data['name'] = name
        if description is not None:
            update_data['description'] = description
        doc_ref.update(update_data)
        return Category.get_by_id(category_id)
    
    @staticmethod
    def delete(category_id):
        """Delete a category and all its weeks."""
        db = get_firestore_client()
        # Delete all weeks for this category
        weeks = db.collection(WEEKS_COLLECTION).where('category_id', '==', category_id).stream()
        for week in weeks:
            Week.delete(week.id)
        # Delete category
        db.collection(CATEGORIES_COLLECTION).document(category_id).delete()


class User:
    """User model for authentication."""
    
    @staticmethod
    def create(username, password, email=None, is_admin=False):
        """Create a new user."""
        db = get_firestore_client()
        user_data = {
            'username': username,
            'password_hash': generate_password_hash(password),
            'email': email,
            'is_admin': is_admin,
            'created_at': datetime.utcnow()
        }
        doc_ref = db.collection(USERS_COLLECTION).document()
        doc_ref.set(user_data)
        return {'id': doc_ref.id, 'username': username, 'email': email, 'is_admin': is_admin}
    
    @staticmethod
    def get_by_username(username):
        """Get user by username."""
        db = get_firestore_client()
        users = db.collection(USERS_COLLECTION).where('username', '==', username).limit(1).stream()
        for user in users:
            data = user.to_dict()
            data['id'] = user.id
            return data
        return None
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID."""
        db = get_firestore_client()
        doc = db.collection(USERS_COLLECTION).document(user_id).get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None
    
    @staticmethod
    def check_password(user_data, password):
        """Check if password matches hash."""
        return check_password_hash(user_data.get('password_hash', ''), password)
    
    @staticmethod
    def update_password(user_id, new_password):
        """Update user password."""
        db = get_firestore_client()
        doc_ref = db.collection(USERS_COLLECTION).document(user_id)
        doc_ref.update({'password_hash': generate_password_hash(new_password)})


class Week:
    """Week model representing a weekly assignment."""
    
    @staticmethod
    def create(category_id, week_number, title, display_name=None, description=None, 
               assignment_url=None, due_date=None, is_active=True):
        """Create a new week."""
        db = get_firestore_client()
        week_data = {
            'category_id': category_id,
            'week_number': week_number,
            'title': title,
            'display_name': display_name,
            'description': description,
            'assignment_url': assignment_url,
            'due_date': due_date,
            'is_active': is_active,
            'created_at': datetime.utcnow()
        }
        doc_ref = db.collection(WEEKS_COLLECTION).document()
        doc_ref.set(week_data)
        return {'id': doc_ref.id, **week_data}
    
    @staticmethod
    def get_all():
        """Get all weeks."""
        db = get_firestore_client()
        weeks = []
        # Fetch all weeks without ordering to avoid composite index requirement
        docs = db.collection(WEEKS_COLLECTION).stream()
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            weeks.append(data)
        
        # Sort client-side to avoid Firestore composite index requirement
        weeks.sort(key=lambda w: (w.get('category_id', ''), w.get('week_number', 0)))
        return weeks
    
    @staticmethod
    def get_by_category(category_id):
        """Get all weeks for a category."""
        db = get_firestore_client()
        weeks = []
        # Avoid Firestore composite index requirement by fetching then sorting client-side.
        docs = db.collection(WEEKS_COLLECTION).where('category_id', '==', category_id).stream()
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            weeks.append(data)
        # Sort by week_number in Python to preserve expected order.
        return sorted(weeks, key=lambda w: w.get('week_number', 0))
    
    @staticmethod
    def get_by_id(week_id):
        """Get week by ID."""
        db = get_firestore_client()
        doc = db.collection(WEEKS_COLLECTION).document(week_id).get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None
    
    @staticmethod
    def get_by_category_and_number(category_id, week_number):
        """Get week by category and week number."""
        db = get_firestore_client()
        weeks = db.collection(WEEKS_COLLECTION)\
            .where('category_id', '==', category_id)\
            .where('week_number', '==', week_number)\
            .limit(1).stream()
        for week in weeks:
            data = week.to_dict()
            data['id'] = week.id
            return data
        return None
    
    @staticmethod
    def update(week_id, **kwargs):
        """Update a week."""
        db = get_firestore_client()
        doc_ref = db.collection(WEEKS_COLLECTION).document(week_id)
        update_data = {k: v for k, v in kwargs.items() if v is not None}
        if update_data:
            doc_ref.update(update_data)
        return Week.get_by_id(week_id)
    
    @staticmethod
    def delete(week_id):
        """Delete a week and all its submissions."""
        db = get_firestore_client()
        # Delete all submissions for this week
        submissions = db.collection(SUBMISSIONS_COLLECTION).where('week_id', '==', week_id).stream()
        for submission in submissions:
            submission.reference.delete()
        # Delete week
        db.collection(WEEKS_COLLECTION).document(week_id).delete()


class Submission:
    """Submission model for student work."""
    
    @staticmethod
    def create(week_id, student_name, project_url, status='pending'):
        """Create a new submission."""
        db = get_firestore_client()
        submission_data = {
            'week_id': week_id,
            'student_name': student_name,
            'project_url': project_url,
            'status': status,
            'admin_comment': None,
            'submitted_at': datetime.utcnow(),
            'modified_by': None
        }
        doc_ref = db.collection(SUBMISSIONS_COLLECTION).document()
        doc_ref.set(submission_data)
        return {'id': doc_ref.id, **submission_data}
    
    @staticmethod
    def get_all():
        """Get all submissions."""
        db = get_firestore_client()
        submissions = []
        docs = db.collection(SUBMISSIONS_COLLECTION).order_by('submitted_at', direction='DESCENDING').stream()
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            submissions.append(data)
        return submissions
    
    @staticmethod
    def get_by_week(week_id):
        """Get all submissions for a week."""
        db = get_firestore_client()
        submissions = []
        docs = db.collection(SUBMISSIONS_COLLECTION)\
            .where('week_id', '==', week_id)\
            .order_by('submitted_at', direction='DESCENDING').stream()
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            submissions.append(data)
        return submissions
    
    @staticmethod
    def get_by_id(submission_id):
        """Get submission by ID."""
        db = get_firestore_client()
        doc = db.collection(SUBMISSIONS_COLLECTION).document(submission_id).get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None
    
    @staticmethod
    def update(submission_id, status=None, admin_comment=None, modified_by=None):
        """Update a submission."""
        db = get_firestore_client()
        doc_ref = db.collection(SUBMISSIONS_COLLECTION).document(submission_id)
        update_data = {}
        if status is not None:
            update_data['status'] = status
        if admin_comment is not None:
            update_data['admin_comment'] = admin_comment
        if modified_by is not None:
            update_data['modified_by'] = modified_by
        if update_data:
            doc_ref.update(update_data)
        return Submission.get_by_id(submission_id)
    
    @staticmethod
    def delete(submission_id):
        """Delete a submission."""
        db = get_firestore_client()
        db.collection(SUBMISSIONS_COLLECTION).document(submission_id).delete()
