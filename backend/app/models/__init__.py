# Import models so they are registered with SQLAlchemy
from app.models.user import User
from app.models.todo import Todo

# This file makes the models directory a Python package
# It also allows us to import models directly from app.models
# For example: from app.models import User, Todo
