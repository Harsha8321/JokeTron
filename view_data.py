from app import app, db
from models import User, Joke

def view_users():
    with app.app_context():
        users = User.query.all()
        if not users:
            print("No users found in the database.")
            return
            
        print("\n=== USERS IN DATABASE ===")
        for user in users:
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Profile complete: {user.is_profile_complete()}")
            print(f"Age: {user.age}")
            print(f"Region: {user.region}")
            print(f"Humor style: {user.humor_style}")
            print(f"Language: {user.language}")
            print(f"Jokes count: {len(user.jokes)}")
            print("-" * 40)

def view_jokes():
    with app.app_context():
        jokes = Joke.query.all()
        if not jokes:
            print("No jokes found in the database.")
            return
            
        print("\n=== JOKES IN DATABASE ===")
        for joke in jokes:
            print(f"ID: {joke.id}")
            print(f"User ID: {joke.user_id}")
            print(f"Content: {joke.content}")
            print(f"Reaction: {joke.reaction}")
            print(f"Created: {joke.created_at}")
            print("-" * 40)


view_users()
view_jokes()