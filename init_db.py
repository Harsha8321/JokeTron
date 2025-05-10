"""
Initialize the SQLite database for JokeTron.
Run this script once to set up the database before starting the application.
"""

import os
import logging
from app import app, db
from models import User, Joke

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Initialize the database with tables."""
    try:
        # Make sure the instance folder exists
        if not os.path.exists('instance'):
            os.makedirs('instance')
            logger.info("Created instance directory")
        
        # Create database tables
        with app.app_context():
            db.create_all()
            logger.info("Database tables created successfully")
        
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        return False

if __name__ == "__main__":
    success = init_database()
    
    if success:
        print("✅ Database initialized successfully!")
        print("You can now run the application with: python run.py")
    else:
        print("❌ Database initialization failed. Check the logs for details.")