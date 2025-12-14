from app import create_app
from db_service import DatabaseService
from datetime import datetime, timedelta

def seed_database():
    """Seed the database with sample data only if it's empty."""
    print("Seeding database...")
    
    db = DatabaseService(use_admin=True)

    # Check if any category exists to prevent re-seeding
    categories = db.get_all_categories()
    if categories:
        print("Database already seeded. Skipping.")
        return

    # Create admin user with encrypted password
    admin_user = db.get_user_by_username('admin')
    if not admin_user:
        db.create_user(username="admin", password="admin", email="admin@sparkrepo.com", is_admin=True)
        print("Created admin user: admin")

    # Create sample categories
    cat1 = db.create_category(name="Beginner Scratch", description="Introductory projects for Scratch")
    cat2 = db.create_category(name="Intermediate Canva", description="Projects for students with some Canva experience")
    print("Added sample categories")

    # Create sample weeks
    # Create weeks 1-6 for Scratch
    for i in range(1, 7):
        db.create_week(
            category_id=cat1['id'],
            week_number=i,
            title=f"Week {i}: {get_week_title(i)}",
            display_name=get_week_title(i),
            description=f"Description for week {i} of beginner Scratch",
            assignment_url=f"https://scratch.mit.edu/projects/example/week{i}",
            due_date=datetime.utcnow() + timedelta(days=i*7)
        )

    # Create weeks 7-12 for Canva
    for i in range(7, 13):
        # Adjust week number for title lookup if necessary, or expand titles
        title_week_num = i - 6  # Reset to 1-6 for lookup in advanced_titles
        db.create_week(
            category_id=cat2['id'],
            week_number=i,
            title=f"Week {i}: {get_week_title(title_week_num, advanced=True)}",
            display_name=get_week_title(title_week_num, advanced=True),
            description=f"Description for week {i} of intermediate Canva",
            assignment_url=f"https://www.canva.com/design/example/week{i}",
            due_date=datetime.utcnow() + timedelta(days=i*7)
        )
    
    print("Added sample weeks")
    
    # Create sample submissions
    week1_cat1 = db.get_week(cat1['id'], 1)
    week1_cat2 = db.get_week(cat2['id'], 7)

    if week1_cat1 and week1_cat2:
        db.create_submission(
            student_name="John Doe",
            week_id=week1_cat1['id'],
            project_type='scratch',
            project_url="https://scratch.mit.edu/projects/123456",
            comment="My first Scratch project!"
        )
        db.create_submission(
            student_name="Jane Smith",
            week_id=week1_cat1['id'],
            project_type='scratch',
            project_url="https://scratch.mit.edu/projects/654321",
            comment="This was fun!"
        )
        db.create_submission(
            student_name="Bob Johnson",
            week_id=week1_cat2['id'],
            project_type='canva',
            project_url="https://www.canva.com/design/DAF-123456/view",
            comment="Intermediate Canva project"
        )
        print("Added sample submissions")
    
    print("Database seeded successfully!")

def get_week_title(week_number, advanced=False):
    """Generate a title for each week based on the week number."""
    beginner_titles = [
        "Introduction to Scratch", "Moving Sprites", "Events and Control", "Variables and Data",
        "Loops and Iteration", "Conditionals", "Custom Blocks", "Lists and Arrays", "Cloning", "Final Project",
        "Bonus Week 1", "Bonus Week 2"
    ]
    advanced_titles = [
        "Advanced Canva Techniques", "Infographics Design", "Social Media Graphics", "Presentation Design",
        "Video Editing Basics", "Brand Kit Creation", "Interactive Elements", "Advanced Data Visualization",
        "Collaborative Design", "Capstone Project", "Advanced Project 1", "Advanced Project 2"
    ]
    titles = advanced_titles if advanced else beginner_titles
    return titles[week_number - 1] if 1 <= week_number <= len(titles) else "Bonus Week"

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # Seed the database
        seed_database()
