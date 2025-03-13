from app import db
from datetime import datetime


class Todo(db.Model):
    """
    Todo model for storing task related details
    """
    __tablename__ = 'todos'  # Explicitly set the table name in the database

    # Define columns (database fields)
    # Unique identifier for each todo
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # Title of the todo
    # Optional longer description
    description = db.Column(db.Text, nullable=True)
    # Whether the todo is completed
    completed = db.Column(db.Boolean, default=False)
    # When the todo was created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)  # When the todo was last updated
    due_date = db.Column(db.DateTime, nullable=True)  # Optional due date

    # Foreign key to link todos to their owner
    # The user.id refers to the id column of the users table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Note: The relationship is defined in the User model with the 'todos' attribute
    # We don't need to define it again here

    def __repr__(self):
        """
        String representation of the Todo object
        This is helpful for debugging
        """
        return f'<Todo {self.id}: {self.title}>'

    def to_dict(self):
        """
        Convert todo object to dictionary for API responses
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'user_id': self.user_id
        }
