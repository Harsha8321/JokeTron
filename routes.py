from flask import render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Joke
import logging
import json
from openai_service import generate_joke as openai_generate_joke

# Home route
@app.route('/')
def index():
    if current_user.is_authenticated:
        if not current_user.is_profile_complete():
            return redirect(url_for('profile'))
        return redirect(url_for('chat'))
    return render_template('index.html')

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('auth.html', current_page='login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth.html', current_page='signup')
        
        # Check if user already exists
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        
        if email_exists:
            flash('Email already in use.', 'danger')
        elif username_exists:
            flash('Username already taken.', 'danger')
        else:
            # Create new user
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            flash('Account created successfully!', 'success')
            login_user(new_user)
            return redirect(url_for('profile'))
    
    return render_template('auth.html', current_page='signup')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Profile routes
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Update user profile
        current_user.age = request.form.get('age')
        current_user.region = request.form.get('region')
        current_user.humor_style = request.form.get('humor_style')
        current_user.language = request.form.get('language')
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('chat'))
        
    return render_template('profile.html')

# Chat and joke routes
@app.route('/chat')
@login_required
def chat():
    if not current_user.is_profile_complete():
        flash('Please complete your profile first!', 'warning')
        return redirect(url_for('profile'))
        
    return render_template('chat.html')

@app.route('/api/generate-joke', methods=['POST'])
@login_required
def generate_joke():
    # Get user profile data to personalize jokes
    user_data = {
        "age": current_user.age,
        "region": current_user.region,
        "humor_style": current_user.humor_style,
        "language": current_user.language
    }
    
    # Get previous jokes to provide context
    previous_jokes = Joke.query.filter_by(user_id=current_user.id).order_by(Joke.created_at.desc()).limit(5).all()
    joke_history = [
        {
            "content": joke.content,
            "reaction": joke.reaction
        } for joke in previous_jokes
    ]
    
    # Generate joke using OpenAI
    joke_text = openai_generate_joke(user_data, joke_history, "Tell me a joke")
    
    # Save joke to database
    new_joke = Joke(content=joke_text, user_id=current_user.id)
    db.session.add(new_joke)
    db.session.commit()
    
    return jsonify({
        "id": new_joke.id,
        "content": new_joke.content,
        "timestamp": new_joke.created_at.strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/api/rate-joke', methods=['POST'])
@login_required
def rate_joke():
    data = request.json
    joke_id = data.get('joke_id')
    reaction = data.get('reaction')  # 'funny', 'neutral', or 'boring'
    
    joke = Joke.query.get(joke_id)
    if joke and joke.user_id == current_user.id:
        joke.reaction = reaction
        db.session.commit()
        return jsonify({"success": True})
    
    return jsonify({"success": False, "error": "Joke not found"}), 404

@app.route('/api/get-jokes', methods=['GET'])
@login_required
def get_jokes():
    jokes = Joke.query.filter_by(user_id=current_user.id).order_by(Joke.created_at.desc()).limit(20).all()
    
    return jsonify({
        "jokes": [
            {
                "id": joke.id,
                "content": joke.content,
                "timestamp": joke.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "reaction": joke.reaction
            } for joke in jokes
        ]
    })

@app.route('/api/clear-jokes', methods=['POST'])
@login_required
def clear_jokes():
    try:
        # Delete all jokes for the current user
        deleted = Joke.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": f"Successfully cleared {deleted} messages from your conversation history."
        })
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error clearing jokes: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to clear conversation history."
        }), 500

@app.route('/api/send-message', methods=['POST'])
@login_required
def send_message():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"success": False, "error": "No message provided"}), 400
    
    # Save user message as a "joke" for tracking in chat history
    user_joke = Joke(content=user_message, user_id=current_user.id)
    db.session.add(user_joke)
    db.session.commit()
    
    # Generate response based on the user's message
    # For now, we'll use predetermined responses based on keywords
    response_text = generate_ai_response(user_message, current_user)
    
    # Save AI response as a joke
    ai_joke = Joke(content=response_text, user_id=current_user.id)
    db.session.add(ai_joke)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "user_message": {
            "id": user_joke.id,
            "content": user_joke.content,
            "timestamp": user_joke.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "is_user": True
        },
        "ai_response": {
            "id": ai_joke.id,
            "content": ai_joke.content,
            "timestamp": ai_joke.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "is_user": False
        }
    })

def generate_ai_response(user_message, user):
    # Get user profile data for personalization
    user_data = {
        "age": user.age,
        "region": user.region,
        "humor_style": user.humor_style,
        "language": user.language
    }
    
    # Get previous jokes for conversation context
    previous_jokes = Joke.query.filter_by(user_id=user.id).order_by(Joke.created_at.desc()).limit(8).all()
    joke_history = [
        {
            "content": joke.content,
            "reaction": joke.reaction
        } for joke in previous_jokes
    ]
    
    try:
        # Use OpenAI to generate a response
        response = openai_generate_joke(user_data, joke_history, user_message)
        return response
    except Exception as e:
        # Fallback responses in case of API error
        logging.error(f"OpenAI API error: {str(e)}")
        message = user_message.lower()
        
        # Simple fallback logic with canned responses
        if "hello" in message or "hi" in message or "hey" in message:
            return f"Hello {user.username}! How can I make you laugh today?"
        elif "joke" in message:
            return "Why did the scarecrow win an award? Because he was outstanding in his field!"
        elif "who are you" in message:
            return "I'm JokeTron, your personal AI comedy assistant. I'm here to brighten your day with humor!"
        else:
            return "Sorry, I'm having a bit of trouble with my comedy circuits. Could you try again with another message?"
