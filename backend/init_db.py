from app import create_app, db
from flask_migrate import Migrate, upgrade


def init_db():
    """Initialize the database with tables"""
    app = create_app()
    with app.app_context():
        # Create database tables
        db.create_all()
        print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()
