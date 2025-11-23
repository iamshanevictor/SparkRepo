"""Supabase database service layer to replace SQLAlchemy models.

This module provides database operations using Supabase client.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash
from supabase_client import get_supabase, get_supabase_admin
from supabase import Client


class DatabaseService:
    """Service class for database operations using Supabase."""
    
    def __init__(self, use_admin: bool = False):
        """Initialize with either regular or admin Supabase client."""
        self.client: Client = get_supabase_admin() if use_admin else get_supabase()
    
    # Category operations
    def get_all_categories(self) -> List[Dict[str, Any]]:
        """Get all categories."""
        response = self.client.table('categories').select('*').order('id', desc=False).execute()
        return [self._format_category(cat) for cat in response.data] if response.data else []
    
    def get_category(self, category_id: int) -> Optional[Dict[str, Any]]:
        """Get a category by ID."""
        response = self.client.table('categories').select('*').eq('id', category_id).execute()
        if response.data:
            return self._format_category(response.data[0])
        return None
    
    def create_category(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Create a new category."""
        data = {
            'name': name,
            'description': description,
            'created_at': datetime.utcnow().isoformat()
        }
        response = self.client.table('categories').insert(data).execute()
        return self._format_category(response.data[0]) if response.data else None
    
    # Week operations
    def get_weeks_by_category(self, category_id: int) -> List[Dict[str, Any]]:
        """Get all weeks for a category."""
        response = self.client.table('weeks').select('*, categories(*)').eq('category_id', category_id).order('week_number', desc=False).execute()
        return [self._format_week(week) for week in response.data] if response.data else []
    
    def get_week(self, category_id: int, week_number: int) -> Optional[Dict[str, Any]]:
        """Get a specific week by category and week number."""
        response = self.client.table('weeks').select('*, categories(*)').eq('category_id', category_id).eq('week_number', week_number).execute()
        if response.data:
            return self._format_week(response.data[0])
        return None
    
    def get_week_by_id(self, week_id: int) -> Optional[Dict[str, Any]]:
        """Get a week by ID."""
        response = self.client.table('weeks').select('*, categories(*)').eq('id', week_id).execute()
        if response.data:
            return self._format_week(response.data[0])
        return None
    
    def get_all_weeks(self) -> List[Dict[str, Any]]:
        """Get all weeks across all categories."""
        response = self.client.table('weeks').select('*, categories(*)').order('category_id', desc=False).order('week_number', desc=False).execute()
        return [self._format_week(week) for week in response.data] if response.data else []
    
    def create_week(self, category_id: int, week_number: int, title: str, 
                   display_name: Optional[str] = None, description: Optional[str] = None,
                   assignment_url: Optional[str] = None, due_date: Optional[datetime] = None,
                   is_active: bool = True) -> Dict[str, Any]:
        """Create a new week."""
        data = {
            'category_id': category_id,
            'week_number': week_number,
            'title': title,
            'display_name': display_name,
            'description': description,
            'assignment_url': assignment_url,
            'due_date': due_date.isoformat() if due_date else None,
            'is_active': is_active,
            'created_at': datetime.utcnow().isoformat(),
            'last_modified': datetime.utcnow().isoformat()
        }
        response = self.client.table('weeks').insert(data).select('*, categories(*)').execute()
        return self._format_week(response.data[0]) if response.data else None
    
    def update_week(self, week_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a week."""
        update_data = {}
        for key, value in kwargs.items():
            if value is not None:
                if isinstance(value, datetime):
                    update_data[key] = value.isoformat()
                else:
                    update_data[key] = value
        update_data['last_modified'] = datetime.utcnow().isoformat()
        
        response = self.client.table('weeks').update(update_data).eq('id', week_id).execute()
        if response.data:
            # Fetch with category relation - need to select with relation
            week_response = self.client.table('weeks').select('*, categories(*)').eq('id', week_id).execute()
            if week_response.data:
                return self._format_week(week_response.data[0])
        return None
    
    def check_week_exists(self, category_id: int, week_number: int) -> bool:
        """Check if a week with the given category_id and week_number exists."""
        response = self.client.table('weeks').select('id').eq('category_id', category_id).eq('week_number', week_number).execute()
        return len(response.data) > 0 if response.data else False
    
    # Submission operations
    def get_submissions_by_week(self, week_id: int) -> List[Dict[str, Any]]:
        """Get all submissions for a week."""
        response = self.client.table('submissions').select('*, weeks(*, categories(*))').eq('week_id', week_id).order('submitted_at', desc=True).execute()
        return [self._format_submission(sub) for sub in response.data] if response.data else []
    
    def get_all_submissions(self, category_id: Optional[int] = None, 
                           week_id: Optional[int] = None, 
                           status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all submissions with optional filters."""
        query = self.client.table('submissions').select('*, weeks(*, categories(*))')
        
        if week_id:
            query = query.eq('week_id', week_id)
        if status:
            query = query.eq('status', status)
        if category_id:
            # Need to filter by category through weeks
            weeks_response = self.client.table('weeks').select('id').eq('category_id', category_id).execute()
            week_ids = [w['id'] for w in weeks_response.data] if weeks_response.data else []
            if week_ids:
                query = query.in_('week_id', week_ids)
            else:
                return []  # No weeks for this category
        
        response = query.order('submitted_at', desc=True).execute()
        return [self._format_submission(sub) for sub in response.data] if response.data else []
    
    def get_submission(self, submission_id: int) -> Optional[Dict[str, Any]]:
        """Get a submission by ID."""
        response = self.client.table('submissions').select('*, weeks(*, categories(*))').eq('id', submission_id).execute()
        if response.data:
            return self._format_submission(response.data[0])
        return None
    
    def create_submission(self, student_name: str, week_id: int, project_url: str,
                         project_type: str = 'scratch', comment: Optional[str] = None) -> Dict[str, Any]:
        """Create a new submission."""
        data = {
            'student_name': student_name,
            'week_id': week_id,
            'project_url': project_url,
            'project_type': project_type,
            'comment': comment,
            'status': 'submitted',
            'submitted_at': datetime.utcnow().isoformat(),
            'last_modified': datetime.utcnow().isoformat()
        }
        response = self.client.table('submissions').insert(data).select('*, weeks(*, categories(*))').execute()
        if response.data:
            return self._format_submission(response.data[0])
        return None
    
    def update_submission(self, submission_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a submission."""
        update_data = {}
        for key, value in kwargs.items():
            if value is not None:
                if isinstance(value, datetime):
                    update_data[key] = value.isoformat()
                else:
                    update_data[key] = value
        update_data['last_modified'] = datetime.utcnow().isoformat()
        
        response = self.client.table('submissions').update(update_data).eq('id', submission_id).execute()
        if response.data:
            # Fetch with relations
            sub_response = self.client.table('submissions').select('*, weeks(*, categories(*))').eq('id', submission_id).execute()
            if sub_response.data:
                return self._format_submission(sub_response.data[0])
        return None
    
    def delete_submission(self, submission_id: int) -> bool:
        """Delete a submission."""
        response = self.client.table('submissions').delete().eq('id', submission_id).execute()
        return True
    
    # User operations
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get a user by username."""
        response = self.client.table('users').select('*').eq('username', username).execute()
        if response.data:
            return self._format_user(response.data[0])
        return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get a user by email."""
        response = self.client.table('users').select('*').eq('email', email).execute()
        if response.data:
            return self._format_user(response.data[0])
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get a user by ID."""
        response = self.client.table('users').select('*').eq('id', user_id).execute()
        if response.data:
            return self._format_user(response.data[0])
        return None
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users."""
        response = self.client.table('users').select('*').order('id', desc=False).execute()
        return [self._format_user(user) for user in response.data] if response.data else []
    
    def create_user(self, username: str, password: str, email: Optional[str] = None,
                   is_admin: bool = False) -> Dict[str, Any]:
        """Create a new user."""
        data = {
            'username': username,
            'password_hash': generate_password_hash(password),
            'email': email,
            'is_admin': is_admin,
            'created_at': datetime.utcnow().isoformat()
        }
        response = self.client.table('users').insert(data).execute()
        return self._format_user(response.data[0]) if response.data else None
    
    def update_user_last_login(self, user_id: int) -> bool:
        """Update user's last login timestamp."""
        self.client.table('users').update({
            'last_login': datetime.utcnow().isoformat()
        }).eq('id', user_id).execute()
        return True
    
    def verify_password(self, password_hash: str, password: str) -> bool:
        """Verify a password against a hash."""
        return check_password_hash(password_hash, password)
    
    # Formatting helpers
    def _format_category(self, cat: Dict[str, Any]) -> Dict[str, Any]:
        """Format category data."""
        return {
            'id': cat['id'],
            'name': cat['name'],
            'description': cat.get('description')
        }
    
    def _format_week(self, week: Dict[str, Any]) -> Dict[str, Any]:
        """Format week data."""
        # Handle nested category relationship from Supabase
        category = None
        if 'categories' in week:
            # Supabase returns nested relationships as a dict or list
            cat_data = week['categories']
            if isinstance(cat_data, dict):
                category = cat_data
            elif isinstance(cat_data, list) and len(cat_data) > 0:
                category = cat_data[0]
        
        return {
            'id': week['id'],
            'category_id': week['category_id'],
            'category_name': category.get('name') if category else None,
            'week_number': week['week_number'],
            'title': week['title'],
            'display_name': week.get('display_name') or week['title'],
            'description': week.get('description'),
            'assignment_url': week.get('assignment_url'),
            'due_date': week.get('due_date'),
            'is_active': week.get('is_active', True),
            'last_modified': week.get('last_modified')
        }
    
    def _format_submission(self, sub: Dict[str, Any]) -> Dict[str, Any]:
        """Format submission data."""
        # Handle nested week relationship from Supabase
        week = None
        if 'weeks' in sub:
            week_data = sub['weeks']
            if isinstance(week_data, dict):
                week = week_data
            elif isinstance(week_data, list) and len(week_data) > 0:
                week = week_data[0]
        
        # Handle nested category within week
        category = None
        if week and isinstance(week, dict) and 'categories' in week:
            cat_data = week['categories']
            if isinstance(cat_data, dict):
                category = cat_data
            elif isinstance(cat_data, list) and len(cat_data) > 0:
                category = cat_data[0]
        
        return {
            'id': sub['id'],
            'student_name': sub['student_name'],
            'week_id': sub['week_id'],
            'week_number': week.get('week_number') if week else None,
            'week_title': (week.get('display_name') or week.get('title')) if week else None,
            'project_type': sub.get('project_type', 'scratch'),
            'project_url': sub['project_url'],
            'comment': sub.get('comment'),
            'admin_comment': sub.get('admin_comment'),
            'status': sub.get('status', 'submitted'),
            'submitted_at': sub.get('submitted_at'),
            'last_modified': sub.get('last_modified')
        }
    
    def _format_user(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Format user data."""
        return {
            'id': user['id'],
            'username': user['username'],
            'email': user.get('email'),
            'is_admin': user.get('is_admin', False),
            'created_at': user.get('created_at'),
            'last_login': user.get('last_login'),
            'password_hash': user.get('password_hash')  # Include for password verification
        }

