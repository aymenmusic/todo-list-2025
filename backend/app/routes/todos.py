from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Todo, User
from app import db
from datetime import datetime

# Create a Blueprint for todo routes
todos_bp = Blueprint('todos', __name__)


@todos_bp.route('/', methods=['GET'])
@jwt_required()
def get_todos():
    """
    Get all todos for the current user
    ---
    Requires JWT token in Authorization header
    """
    # Get user ID from JWT token
    user_id = get_jwt_identity()
    # Convert string ID to integer if needed
    user_id = int(user_id) if isinstance(user_id, str) else user_id

    # Get query parameters for filtering
    completed = request.args.get('completed')

    # Start with a base query for the user's todos
    query = Todo.query.filter_by(user_id=user_id)

    # Apply filters if provided
    if completed is not None:
        completed = completed.lower() == 'true'
        query = query.filter_by(completed=completed)

    # Execute query and get todos
    todos = query.order_by(Todo.created_at.desc()).all()

    # Return todos as JSON
    return jsonify([todo.to_dict() for todo in todos]), 200


@todos_bp.route('/', methods=['POST'])
@jwt_required()
def create_todo():
    """
    Create a new todo
    ---
    Request body:
    {
        "title": "Learn Flask",
        "description": "Study Flask framework for web development",
        "due_date": "2023-12-31T23:59:59" (optional)
    }
    """
    # Get user ID from JWT token
    user_id = get_jwt_identity()
    # Convert string ID to integer if needed
    user_id = int(user_id) if isinstance(user_id, str) else user_id

    # Get data from request
    data = request.get_json()

    # Validate required fields
    if 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    # Parse due date if provided
    due_date = None
    if 'due_date' in data and data['due_date']:
        try:
            due_date = datetime.fromisoformat(data['due_date'])
        except ValueError:
            return jsonify({'error': 'Invalid due date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400

    # Create new todo
    todo = Todo(
        title=data['title'],
        description=data.get('description', ''),
        due_date=due_date,
        user_id=user_id
    )

    # Save todo to database
    db.session.add(todo)
    db.session.commit()

    # Return created todo
    return jsonify(todo.to_dict()), 201


@todos_bp.route('/<int:todo_id>', methods=['GET'])
@jwt_required()
def get_todo(todo_id):
    """
    Get a specific todo by ID
    """
    # Get user ID from JWT token
    user_id = get_jwt_identity()
    # Convert string ID to integer if needed
    user_id = int(user_id) if isinstance(user_id, str) else user_id

    # Find todo by ID and user ID
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()

    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    # Return todo as JSON
    return jsonify(todo.to_dict()), 200


@todos_bp.route('/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    """
    Update a specific todo
    ---
    Request body:
    {
        "title": "Updated title",
        "description": "Updated description",
        "completed": true,
        "due_date": "2023-12-31T23:59:59"
    }
    """
    # Get user ID from JWT token
    user_id = get_jwt_identity()
    # Convert string ID to integer if needed
    user_id = int(user_id) if isinstance(user_id, str) else user_id

    # Find todo by ID and user ID
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()

    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    # Get data from request
    data = request.get_json()

    # Update todo fields if provided
    if 'title' in data:
        todo.title = data['title']

    if 'description' in data:
        todo.description = data['description']

    if 'completed' in data:
        todo.completed = bool(data['completed'])

    if 'due_date' in data:
        if data['due_date'] is None:
            todo.due_date = None
        else:
            try:
                todo.due_date = datetime.fromisoformat(data['due_date'])
            except ValueError:
                return jsonify({'error': 'Invalid due date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400

    # Update the updated_at timestamp
    todo.updated_at = datetime.utcnow()

    # Save changes to database
    db.session.commit()

    # Return updated todo
    return jsonify(todo.to_dict()), 200


@todos_bp.route('/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    """
    Delete a specific todo
    """
    # Get user ID from JWT token
    user_id = get_jwt_identity()
    # Convert string ID to integer if needed
    user_id = int(user_id) if isinstance(user_id, str) else user_id

    # Find todo by ID and user ID
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()

    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    # Delete todo from database
    db.session.delete(todo)
    db.session.commit()

    # Return success message
