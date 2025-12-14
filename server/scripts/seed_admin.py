"""
Seed or update an admin user with username 'admin' and password 'admin'.
Use ONLY for local development.
"""
from app import create_app
from db_service import DatabaseService


def main():
    app = create_app()
    with app.app_context():
        db = DatabaseService(use_admin=True)
        user = db.get_user_by_username("admin")
        if user is None:
            db.create_user(username="admin", password="admin", is_admin=True)
            print("[seed_admin] Created admin user 'admin' with password 'admin'.")
        else:
            # Note: Supabase doesn't have a direct update method in our service
            # For now, we'll just print a message. In production, you'd want to add an update_user method
            print("[seed_admin] Admin user 'admin' already exists. To reset password, delete and recreate the user.")


if __name__ == "__main__":
    main()
