from flask_bcrypt import Bcrypt  # Import bcrypt for password hashing
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for database interaction
from flask import session  # Import session for session management (to store logged-in user ID)

# Initialize Bcrypt and SQLAlchemy instances
bcrypt = Bcrypt()
db = SQLAlchemy()

# Define the User model for the database
class User(db.Model):
    __tablename__ = 'users'  # Define the table name as 'users'
    
    # Define columns in the 'users' table
    id = db.Column(db.Integer, primary_key=True)  # Primary key for user (auto-incrementing integer)
    username = db.Column(db.String(80), unique=True, nullable=False)  # Unique username column (max 80 chars)
    password_hash = db.Column(db.String(200), nullable=False)  # Hashed password column (max 200 chars)

    def __init__(self, username, password):
        # Initialize a new user with a username and a hashed password
        self.username = username
        # Use bcrypt to hash the password and store it
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

# Function to register a new user
def register_user(username, password):
    # Check if the user already exists in the database
    if User.query.filter_by(username=username).first():
        # Raise an error if the username is already taken
        raise ValueError("User already exists")
    
    # Create a new user object and hash their password
    new_user = User(username, password)
    # Add the new user to the database session
    db.session.add(new_user)
    # Commit the transaction to save the new user to the database
    db.session.commit()

# Function to authenticate a user during login
def authenticate_user(username, password):
    # Query the database for a user with the given username
    user = User.query.filter_by(username=username).first()
    # If the user exists and the password matches the hash
    if user and bcrypt.check_password_hash(user.password_hash, password):
        # Store the user ID in the session for authentication
        session['user_id'] = user.id
        # Return True indicating successful authentication
        return True
    # Return False if the username does not exist or the password is incorrect
    return False

# Function to log out the user
def logout_user():
    # Remove the user ID from the session to log the user out
    session.pop('user_id', None)

# Function to check if the user is authenticated (logged in)
def is_authenticated():
    # Check if the user ID exists in the session (i.e., the user is logged in)
    return 'user_id' in session
