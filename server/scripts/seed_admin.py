"""
Seed or update an admin user with username 'admin' and password 'admin'.
Use ONLY for local development.
"""
from app import create_app
from models import db, User


def main():
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(username="admin").first()
        if user is None:
            user = User(username="admin", is_admin=True)
            user.set_password("admin")
            db.session.add(user)
            db.session.commit()
            print("[seed_admin] Created admin user 'admin' with password 'admin'.")
        else:
            user.is_admin = True
            user.set_password("admin")
            db.session.commit()
            print("[seed_admin] Updated existing 'admin' user and reset password to 'admin'.")


if __name__ == "__main__":
    main()
