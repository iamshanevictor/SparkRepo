"""Seed Firestore with sample categories, weeks, and a couple submissions.

Run for local development only:
  python -m server.scripts.seed_firestore
"""
from datetime import datetime, timedelta

from ..app import create_app
from ..models import Category, Week, Submission


def seed():
    app = create_app()
    with app.app_context():
        categories = Category.get_all()
        if categories:
            print("[seed] Categories already exist; skipping seed.")
            return

        print("[seed] Seeding Firestore with sample data...")

        # Create sample categories
        scratch = Category.create(name="Scratch Projects", description="Learn coding with Scratch")
        canva = Category.create(name="Canva Design", description="Learn design with Canva")
        print(f"[seed] Created categories: {scratch['name']}, {canva['name']}")

        # Create sample weeks for Scratch (1-3)
        for i, title in enumerate([
            "Week 1: Introduction to Scratch",
            "Week 2: Events and Control",
            "Week 3: Variables and Loops",
        ], start=1):
            Week.create(
                category_id=scratch['id'],
                week_number=i,
                title=title,
                display_name=title,
                description=f"Activities for {title}",
                assignment_url=f"https://scratch.mit.edu/projects/example/week{i}",
                due_date=datetime.utcnow() + timedelta(days=i * 7),
                is_active=True,
            )

        # Create sample weeks for Canva (4-5)
        for i, title in enumerate([
            "Week 4: Canva Basics",
            "Week 5: Social Graphics",
        ], start=4):
            Week.create(
                category_id=canva['id'],
                week_number=i,
                title=title,
                display_name=title,
                description=f"Activities for {title}",
                assignment_url=f"https://www.canva.com/design/example/week{i}",
                due_date=datetime.utcnow() + timedelta(days=i * 7),
                is_active=True,
            )

        # Add a couple of sample submissions to Scratch Week 1
        all_weeks = Week.get_by_category(scratch['id'])
        week1 = next((w for w in all_weeks if w.get('week_number') == 1), None)
        if week1:
            Submission.create(
                week_id=week1['id'],
                student_name="John Doe",
                project_url="https://scratch.mit.edu/projects/123",
                status="pending",
            )
            Submission.create(
                week_id=week1['id'],
                student_name="Jane Smith",
                project_url="https://scratch.mit.edu/projects/456",
                status="pending",
            )

        print("[seed] Firestore seed complete.")


if __name__ == "__main__":
    seed()
