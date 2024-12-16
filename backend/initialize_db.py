import os
import sys

# Add the current directory to the system path for importing modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Import the Flask app and SQLAlchemy instance
from api import app, db

# Create all database tables within the app's context
with app.app_context():  # Ensure app context is available
    db.create_all()  # This will create all tables defined in models.py

print("Database tables created successfully.")  # Confirmation message
