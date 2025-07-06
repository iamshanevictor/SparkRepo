"""
Script to forcefully reset the database by deleting the file and recreating it
"""
import os
import sys
import time
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

# Database file path
DB_FILE = "sparkrepo.db"

def force_delete_db():
    """Forcefully delete the database file"""
    print(f"Attempting to delete database file: {DB_FILE}")
    
    # Try to delete the file multiple times if needed
    for attempt in range(5):
        try:
            if os.path.exists(DB_FILE):
                os.remove(DB_FILE)
                print(f"Successfully deleted database file on attempt {attempt+1}")
                return True
            else:
                print("Database file does not exist, nothing to delete")
                return True
        except Exception as e:
            print(f"Error deleting database file (attempt {attempt+1}): {e}")
            time.sleep(1)  # Wait a bit before retrying
    
    print("Failed to delete database file after multiple attempts")
    return False

def create_fresh_db():
    """Create a fresh database with all tables"""
    # Create a minimal Flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_FILE}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize SQLAlchemy
    db = SQLAlchemy(app)
    
    # Define models directly in this script to avoid import issues
    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), unique=True, nullable=False)
        password_hash = db.Column(db.String(256), nullable=False)
        email = db.Column(db.String(100), unique=True, nullable=True)
        is_admin = db.Column(db.Boolean, default=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        last_login = db.Column(db.DateTime, nullable=True)
        
        def set_password(self, password):
            self.password_hash = generate_password_hash(password)
    
    class Class(db.Model):
        __tablename__ = 'classes'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        description = db.Column(db.Text, nullable=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    class Week(db.Model):
        __tablename__ = 'weeks'
        id = db.Column(db.Integer, primary_key=True)
        class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
        week_number = db.Column(db.Integer, nullable=False)
        title = db.Column(db.String(100), nullable=False)
        display_name = db.Column(db.String(100), nullable=True)
        description = db.Column(db.Text, nullable=True)
        assignment_url = db.Column(db.String(255), nullable=True)
        due_date = db.Column(db.DateTime, nullable=True)
        is_active = db.Column(db.Boolean, default=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        __table_args__ = (
            db.UniqueConstraint('class_id', 'week_number', name='unique_class_week'),
        )
    
    class Student(db.Model):
        __tablename__ = 'students'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(100), nullable=False, unique=True)
        class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    class Submission(db.Model):
        __tablename__ = 'submissions'
        id = db.Column(db.Integer, primary_key=True)
        student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
        week_id = db.Column(db.Integer, db.ForeignKey('weeks.id'), nullable=False)
        project_url = db.Column(db.String(255), nullable=False)
        comment = db.Column(db.Text, nullable=True)
        admin_comment = db.Column(db.Text, nullable=True)
        status = db.Column(db.String(20), default='submitted')
        submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
        last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        modified_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
        
        __table_args__ = (
            db.UniqueConstraint('student_id', 'week_id', name='unique_student_week_submission'),
        )
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Created database schema")
        
        # Create admin user
        admin = User(
            username="admin",
                        email="admin@sparkrepo.com",
            is_admin=True,
            created_at=datetime.utcnow()
        )
        admin.set_password("admin")
        db.session.add(admin)
        db.session.commit()
        print("Created admin user (username: admin, password: admin)")
        
        # Create sample data
        create_sample_data(db, Class, Week, Student, Submission)

def create_sample_data(db, Class, Week, Student, Submission):
    """Create sample data for the application"""
    # Create sample classes
    class1 = Class(name="Coding for Kids 001 (2025)", description="Beginner coding class")
    class2 = Class(name="Coding for Kids 002 (2025)", description="Intermediate coding class")
    
    db.session.add_all([class1, class2])
    db.session.commit()
    
    # Create sample weeks
    weeks = []
    for i in range(1, 11):  # 10 weeks for each class
        # Class 1 weeks
        weeks.append(Week(
            class_id=class1.id,
            week_number=i,
            title=f"Week {i}: {get_week_title(i)}",
            display_name=get_week_title(i),
            description=f"Description for week {i} of beginner class",
            assignment_url=f"https://scratch.mit.edu/projects/example/week{i}",
            due_date=datetime.utcnow() + timedelta(days=i*7),
            is_active=True
        ))
        
        # Class 2 weeks
        weeks.append(Week(
            class_id=class2.id,
            week_number=i,
            title=f"Week {i}: {get_week_title(i, advanced=True)}",
            display_name=get_week_title(i, advanced=True),
            description=f"Description for week {i} of intermediate class",
            assignment_url=f"https://scratch.mit.edu/projects/example/advanced/week{i}",
            due_date=datetime.utcnow() + timedelta(days=i*7),
            is_active=True
        ))
    
    db.session.add_all(weeks)
    db.session.commit()
    
    # Create sample students
    students = [
        Student(name="John Doe", email="john@example.com", class_id=class1.id),
        Student(name="Jane Smith", email="jane@example.com", class_id=class1.id),
        Student(name="Bob Johnson", email="bob@example.com", class_id=class2.id),
        Student(name="Alice Brown", email="alice@example.com", class_id=class2.id)
    ]
    
    db.session.add_all(students)
    db.session.commit()
    
    # Create sample submissions
    submissions = [
        Submission(
            student_id=students[0].id,
            week_id=weeks[0].id,
            project_url="https://scratch.mit.edu/projects/123456",
            comment="My first Scratch project!",
            status="submitted",
            submitted_at=datetime.utcnow() - timedelta(days=2)
        ),
        Submission(
            student_id=students[1].id,
            week_id=weeks[0].id,
            project_url="https://scratch.mit.edu/projects/654321",
            comment="This was fun!",
            status="submitted",
            submitted_at=datetime.utcnow() - timedelta(days=1)
        ),
        Submission(
            student_id=students[2].id,
            week_id=weeks[10].id,  # Week 1 for class 2
            project_url="https://scratch.mit.edu/projects/789012",
            comment="Intermediate project",
            status="submitted",
            submitted_at=datetime.utcnow() - timedelta(hours=12)
        )
    ]
    
    db.session.add_all(submissions)
    db.session.commit()
    print("Added sample data")

def get_week_title(week_number, advanced=False):
    """Generate a title for each week based on the week number."""
    beginner_titles = [
        "Introduction to Scratch",
        "Moving Sprites",
        "Events and Control",
        "Variables and Data",
        "Loops and Iteration",
        "Conditionals",
        "Custom Blocks",
        "Lists and Arrays",
        "Cloning",
        "Final Project"
    ]
    
    advanced_titles = [
        "Advanced Scratch Concepts",
        "Complex Movement Patterns",
        "Event Broadcasting",
        "Data Structures",
        "Nested Loops",
        "Complex Conditionals",
        "Functions and Parameters",
        "Advanced Data Structures",
        "Object-Oriented Programming",
        "Capstone Project"
    ]
    
    if week_number <= 10:
        return advanced_titles[week_number-1] if advanced else beginner_titles[week_number-1]
    else:
        return "Bonus Week"

def main():
    """Main function to reset the database"""
    print("Starting forced database reset...")
    
    # Step 1: Delete the existing database
    if not force_delete_db():
        print("Failed to delete database, aborting")
        sys.exit(1)
    
    # Step 2: Create a fresh database
    try:
        create_fresh_db()
        print("Database reset successful!")
    except Exception as e:
        print(f"Error creating fresh database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
