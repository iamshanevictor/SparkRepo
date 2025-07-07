from app import create_app
from models import db, Category, Week, Submission, User
from datetime import datetime, timedelta

def seed_database():
    """Seed the database with sample data only if it's empty."""
    print("Seeding database...")

    # Check if any category exists to prevent re-seeding
    if db.session.query(Category).first():
        print("Database already seeded. Skipping.")
        return

    # Create admin user with encrypted password
    if not User.query.filter_by(username='admin').first():
        admin = User(username="admin", email="admin@sparkrepo.com", is_admin=True)
        admin.set_password("admin")
        db.session.add(admin)
        print("Created admin user: admin")

    # Create sample categories
    cat1 = Category(name="Beginner Scratch", description="Introductory projects for Scratch")
    cat2 = Category(name="Intermediate Canva", description="Projects for students with some Canva experience")
    db.session.add_all([cat1, cat2])
    
    # Commit users and categories to get their IDs
    db.session.commit()
    print("Added sample categories")

    # Create sample weeks
    weeks = []
    for i in range(1, 11):  # 10 weeks for each category
        # Category 1 weeks
        weeks.append(Week(
            category_id=cat1.id,
            week_number=i,
            title=f"Week {i}: {get_week_title(i)}",
            display_name=get_week_title(i),
            description=f"Description for week {i} of beginner Scratch",
            assignment_url=f"https://scratch.mit.edu/projects/example/week{i}",
            due_date=datetime.utcnow() + timedelta(days=i*7)
        ))
        
        # Category 2 weeks
        weeks.append(Week(
            category_id=cat2.id,
            week_number=i,
            title=f"Week {i}: {get_week_title(i, advanced=True)}",
            display_name=get_week_title(i, advanced=True),
            description=f"Description for week {i} of intermediate Canva",
            assignment_url=f"https://www.canva.com/design/example/week{i}",
            due_date=datetime.utcnow() + timedelta(days=i*7)
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
                student_name="John Doe",
                week_id=week1_cat1.id,
                project_type='scratch',
                project_url="https://scratch.mit.edu/projects/123456",
                comment="My first Scratch project!",
                submitted_at=datetime.utcnow() - timedelta(days=2)
            ),
            Submission(
                student_name="Jane Smith",
                week_id=week1_cat1.id,
                project_type='scratch',
                project_url="https://scratch.mit.edu/projects/654321",
                comment="This was fun!",
                submitted_at=datetime.utcnow() - timedelta(days=1)
            ),
            Submission(
                student_name="Bob Johnson",
                week_id=week1_cat2.id,
                project_type='canva',
                project_url="https://www.canva.com/design/DAF-123456/view",
                comment="Intermediate Canva project",
                submitted_at=datetime.utcnow() - timedelta(hours=12)
            )
        ]
        db.session.add_all(submissions)
        db.session.commit()
        print("Added sample submissions")
    
    print("Database seeded successfully!")

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

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        # Seed the database
        seed_database()
