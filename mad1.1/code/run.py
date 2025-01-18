from app import create_app, db

# Create the Flask app instance
app = create_app()

# Automatically create the database tables if they don't exist
with app.app_context():
    db.create_all()

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
