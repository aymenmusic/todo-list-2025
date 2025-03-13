from app import create_app

# Create the Flask application using the factory function
app = create_app()

if __name__ == '__main__':
    # Run the application in debug mode when this script is executed directly
    # Debug mode provides detailed error messages and auto-reloads when code changes
    app.run(debug=True)
