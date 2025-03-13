# Todo List Application with User Authentication

A full-stack todo list application with user authentication built using Flask (backend) and React with TypeScript (frontend).

## Project Structure

The project is organized into two main directories:

- **backend/**: Flask API with SQLite database
- **frontend/**: React TypeScript application with Tailwind CSS

## Features

- User registration and authentication
- Create, read, update, and delete todo items
- Filter todos by completion status
- Responsive UI with Tailwind CSS

## Backend Technologies

- Flask: Web framework
- Flask-SQLAlchemy: ORM for database operations
- Flask-JWT-Extended: JWT authentication
- SQLite: Database (for development)

## Frontend Technologies

- React: UI library
- TypeScript: Type-safe JavaScript
- Tailwind CSS: Utility-first CSS framework
- React Router: Client-side routing
- Axios: HTTP client

## Getting Started

### Backend Setup

1. Navigate to the backend directory:

   ```
   cd backend
   ```

2. Create a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Initialize the database:

   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. Run the development server:
   ```
   python run.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:

   ```
   cd frontend
   ```

2. Install dependencies:

   ```
   npm install
   ```

3. Run the development server:
   ```
   npm start
   ```

## API Endpoints

### Authentication

- `POST /api/auth/register`: Register a new user
- `POST /api/auth/login`: Login a user
- `GET /api/auth/me`: Get current user information

### Todos

- `GET /api/todos/`: Get all todos for the current user
- `POST /api/todos/`: Create a new todo
- `GET /api/todos/<id>`: Get a specific todo
- `PUT /api/todos/<id>`: Update a specific todo
- `DELETE /api/todos/<id>`: Delete a specific todo
