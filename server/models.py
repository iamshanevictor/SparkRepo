from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Category(db.Model):
    """Category model representing a project type, e.g., Scratch or Canva."""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    weeks = db.relationship('Week', back_populates='category', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


class User(db.Model):
    """User model for authentication, including admin users."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }


class Week(db.Model):
    """Week model representing a weekly assignment."""
    __tablename__ = 'weeks'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    display_name = db.Column(db.String(100), nullable=True)  # Added for flexible naming
    description = db.Column(db.Text, nullable=True)
    assignment_url = db.Column(db.String(255), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)  # Added to control visibility
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = db.relationship('Category', back_populates='weeks')
    submissions = db.relationship('Submission', back_populates='week', cascade='all, delete-orphan')
    
    __table_args__ = (
        db.UniqueConstraint('category_id', 'week_number', name='unique_category_week'),
    )
    
    def __repr__(self):
        return f'<Week {self.week_number} for Category {self.category_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'week_number': self.week_number,
            'title': self.title,
            'display_name': self.display_name or self.title,
            'description': self.description,
            'assignment_url': self.assignment_url,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'is_active': self.is_active,
            'last_modified': self.last_modified.isoformat()
        }


class Student(db.Model):
    """Student model representing a student user."""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    submissions = db.relationship('Submission', back_populates='student', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Student {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


class Submission(db.Model):
    """Submission model representing a student's project link submission."""
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    week_id = db.Column(db.Integer, db.ForeignKey('weeks.id'), nullable=False)
    project_type = db.Column(db.String(50), nullable=False, default='scratch')  # 'scratch' or 'canva'
    project_url = db.Column(db.String(255), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    admin_comment = db.Column(db.Text, nullable=True)  # Added for admin feedback
    status = db.Column(db.String(20), default='submitted')  # e.g., 'submitted', 'approved', 'rejected'
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Track who modified it
    
    # Relationships
    student = db.relationship('Student', back_populates='submissions')
    week = db.relationship('Week', back_populates='submissions')
    admin = db.relationship('User', foreign_keys=[modified_by], backref='modified_submissions')
    
    __table_args__ = (
        db.UniqueConstraint('student_id', 'week_id', name='unique_student_week_submission'),
    )
    
    def __repr__(self):
        return f'<Submission by Student {self.student_id} for Week {self.week.week_number}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.name,
            'week_id': self.week_id,
            'week_number': self.week.week_number,
            'week_title': self.week.display_name or self.week.title,
            'project_type': self.project_type,
            'project_url': self.project_url,
            'comment': self.comment,
            'admin_comment': self.admin_comment,
            'status': self.status,
            'submitted_at': self.submitted_at.isoformat(),
            'last_modified': self.last_modified.isoformat()
        }


class ProjectSubmission(db.Model):
    """A simple model for project submissions."""
    __tablename__ = 'project_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    project_link = db.Column(db.String(255), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProjectSubmission {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'project_link': self.project_link,
            'submitted_at': self.submitted_at.isoformat()
        }
