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
    
    # Get the absolute path for the database file
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_file = os.path.join(basedir, "sparkrepo.db")
    
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
    from models import Category, Week
    from datetime import timedelta
    
    with app.app_context():
        # Create sample categories
        scratch_category = Category(name="Scratch", description="Scratch projects")
        canva_category = Category(name="Canva", description="Canva projects")
        
        db.session.add_all([scratch_category, canva_category])
        db.session.commit()
        
        # Create sample weeks for each category
        weeks = []
        for i in range(1, 11):  # 10 weeks for each category
            # Scratch weeks
            weeks.append(Week(
                category_id=scratch_category.id,
                week_number=i,
                title=f"Week {i}: {get_week_title(i)}",
                display_name=get_week_title(i),
                description=f"Description for week {i} of Scratch projects",
                assignment_url=f"https://scratch.mit.edu/projects/example/week{i}",
                due_date=datetime.utcnow() + timedelta(days=i*7),
                is_active=True
            ))
            
            # Canva weeks
            weeks.append(Week(
                category_id=canva_category.id,
                week_number=i,
                title=f"Week {i}: {get_week_title(i, advanced=True)}",
                display_name=get_week_title(i, advanced=True),
                description=f"Description for week {i} of Canva projects",
                assignment_url=f"https://www.canva.com/design/example/week{i}",
                due_date=datetime.utcnow() + timedelta(days=i*7),
                is_active=True
            ))
        
        db.session.add_all(weeks)
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
