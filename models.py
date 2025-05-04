from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # User profile information
    age = db.Column(db.Integer, nullable=True)
    region = db.Column(db.String(64), nullable=True)
    humor_style = db.Column(db.String(64), nullable=True)
    language = db.Column(db.String(32), nullable=True)
    
    # Relationship with jokes
    jokes = db.relationship('Joke', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def is_profile_complete(self):
        return all([self.age, self.region, self.humor_style, self.language])

class Joke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reaction = db.Column(db.String(10), nullable=True)  # 'funny', 'neutral', or 'boring'
    
    def __repr__(self):
        return f'<Joke {self.id}>'
