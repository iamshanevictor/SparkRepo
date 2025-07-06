"""
Script to reset the database and recreate it with the current schema
"""
import os
import sys
import sqlite3
from app import create_app
from models import db, User
from datetime import datetime

def reset_database():
    """Delete the existing database and recreate it with the current schema"""
    print("Resetting database...")
    
    # Get the database file path
    db_file = "sparkrepo.db"
    
    # Delete the database file if it exists
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
            print(f"Deleted existing database file: {db_file}")
        except Exception as e:
            print(f"Error deleting database file: {e}")
            sys.exit(1)
    
    # Create the application context
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Created new database schema")
        
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
        create_sample_data(app)
        print("Database reset complete!")

def create_sample_data(app):
    """Create sample data for the application"""
    from models import Class, Week, Student, Submission
    from datetime import timedelta
    
    with app.app_context():
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

if __name__ == "__main__":
    reset_database()
