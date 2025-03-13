from app import create_app

if __name__ == "__main__":
    app = create_app()
    # Changed port to 5001 to avoid conflicts
    app.run(debug=True, host='0.0.0.0', port=5001)
