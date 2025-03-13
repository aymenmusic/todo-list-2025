from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):  # db.Model is used to inherit from the SQLAlchemy class
    """
    User model for storing user related details
    """
    __tablename__ = 'users'  # Explicitly set the table name in the database. If not explicitly set then SQLAlchemy will automatically generate a table name by converting the class name from CamelCase to snake_case (so User becomes user, singular not plural. For convention purposes we need it to be plural (users, todos, products, etc))

    # Define columns (database fields)
    # Unique identifier for each user
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True,
                         nullable=False, index=True)  # Username must be unique
    email = db.Column(db.String(120), unique=True,
                      nullable=False, index=True)  # Email must be unique
    # Store password hash, never the actual password
    password_hash = db.Column(db.String(128), nullable=False)
    # When the user was created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Define relationship with Todo model (we'll create this next)
    # This creates a virtual 'todos' property on User instances
    # cascade='all, delete-orphan' means if a user is deleted, their todos are also deleted
    todos = db.relationship('Todo', backref='user',
                            lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        """
        String representation of the User object
        This is helpful for debugging - when you print a User object, this is what you'll see
        """
        return f'<User {self.username}>'

    def set_password(self, password):
        """
        Set password hash from plain text password
        This ensures we never store plain text passwords
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if provided password matches the hash
        Returns True if password is correct, False otherwise
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        Convert user object to dictionary for API responses
        Excludes sensitive information like password_hash
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
