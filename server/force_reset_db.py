"""
Script to forcefully reset the database by dropping all tables and recreating them.
This script uses the models from the main application to ensure schema consistency.
"""
import sys
from flask import Flask
from datetime import datetime, timedelta

# Import the db instance and models from the main application
from models import db, User, Category, Week, Submission

def create_app():
    """Create a minimal Flask app to establish an application context."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sparkrepo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def create_sample_data():
    """Create sample data for the application."""
    print("Creating sample data...")

    # Create categories
    cat1 = Category(name="Beginner Scratch", description="Introductory projects for Scratch")
    cat2 = Category(name="Intermediate Canva", description="Projects for students with some Canva experience")
    db.session.add_all([cat1, cat2])
    db.session.commit()
    print("Added sample categories")

    # Create weeks for each category
    weeks = []
    for i in range(1, 11):
        weeks.append(Week(
            category_id=cat1.id, week_number=i, title=f"Week {i}: {get_week_title(i)}",
            display_name=get_week_title(i), description=f"Description for week {i} of beginner Scratch",
            assignment_url=f"https://scratch.mit.edu/projects/example/week{i}",
            due_date=datetime.utcnow() + timedelta(days=i*7), is_active=True
        ))
        weeks.append(Week(
            category_id=cat2.id, week_number=i, title=f"Week {i}: {get_week_title(i, advanced=True)}",
            display_name=get_week_title(i, advanced=True), description=f"Description for week {i} of intermediate Canva",
            assignment_url=f"https://www.canva.com/design/example/week{i}",
            due_date=datetime.utcnow() + timedelta(days=i*7), is_active=True
        ))
    
    db.session.add_all(weeks)
    db.session.commit()
    print("Added sample weeks")

    # Create sample submissions
    week1_cat1 = Week.query.filter_by(category_id=cat1.id, week_number=1).first()
    week1_cat2 = Week.query.filter_by(category_id=cat2.id, week_number=1).first()

    if week1_cat1 and week1_cat2:
        submissions = [
            Submission(
                student_name="John Doe", week_id=week1_cat1.id, project_type='scratch',
                project_url="https://scratch.mit.edu/projects/123456", comment="My first Scratch project!",
                status="submitted", submitted_at=datetime.utcnow() - timedelta(days=2)
            ),
            Submission(
                student_name="Jane Smith", week_id=week1_cat1.id, project_type='scratch',
                project_url="https://scratch.mit.edu/projects/654321", comment="This was fun!",
                status="submitted", submitted_at=datetime.utcnow() - timedelta(days=1)
            ),
            Submission(
                student_name="Bob Johnson", week_id=week1_cat2.id, project_type='canva',
                project_url="https://www.canva.com/design/DAF-123456/view", comment="Intermediate Canva project",
                status="submitted", submitted_at=datetime.utcnow() - timedelta(hours=12)
            )
        ]
        db.session.add_all(submissions)
        db.session.commit()
        print("Added sample submissions")

    # Create an admin user
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin', email='admin@example.com', is_admin=True)
        admin_user.set_password('admin')
        db.session.add(admin_user)
        db.session.commit()
        print("Added admin user (admin/admin)")

def get_week_title(week_number, advanced=False):
    """Generate a title for each week based on the week number."""
    beginner_titles = [
        "Introduction to Scratch", "Moving Sprites", "Events and Control", "Variables and Data",
        "Loops and Iteration", "Conditionals", "Custom Blocks", "Lists and Arrays", "Cloning", "Final Project"
    ]
    advanced_titles = [
        "Advanced Canva Techniques", "Infographics Design", "Social Media Graphics", "Presentation Design",
        "Video Editing Basics", "Brand Kit Creation", "Interactive Elements", "Advanced Data Visualization",
        "Collaborative Design", "Capstone Project"
    ]
    titles = advanced_titles if advanced else beginner_titles
    return titles[week_number - 1] if 1 <= week_number <= len(titles) else "Bonus Week"

def main():
    """Main function to reset the database."""
    app = create_app()
    with app.app_context():
        print("Starting database reset...")
        try:
            # Step 1: Drop all tables
            print("Dropping all tables...")
            db.drop_all()
            print("Tables dropped.")
            
            # Step 2: Create all tables
            print("Creating all tables...")
            db.create_all()
            print("Tables created.")
            
            # Step 3: Create sample data
            create_sample_data()
            
            print("Database reset successful!")
        except Exception as e:
            print(f"An error occurred during database reset: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
