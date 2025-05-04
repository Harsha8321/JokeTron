# JokeTron - Personalized Joke Platform (SQLite Version)

JokeTron is a responsive, chat-based joke platform that offers personalized humor experiences through intuitive user authentication and interactive joke delivery.

## Features
- Dark mode professional interface
- Unified authentication system
- Real-time user feedback collection
- Dynamic joke presentation
- Personalization based on user preferences
- **Serverless SQLite database** - no PostgreSQL required!

## Installation

1. Clone or extract this repository to your local machine
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python run.py
   ```
   
5. Access the application at http://localhost:5000

## Notes
- This version uses SQLite instead of PostgreSQL, making it easier to run locally
- The database will automatically be created as joketron.db in your project folder
- No additional database configuration is required

## Technologies Used
- Flask
- Flask-SQLAlchemy with SQLite
- Flask-Login
- TailwindCSS
- JavaScript

## License
MIT
