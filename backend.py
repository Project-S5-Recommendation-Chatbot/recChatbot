#!/usr/bin/env python3
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from authentication import db, bcrypt, register_user, authenticate_user, logout_user, is_authenticated
from llm.llm_manager import LLMManager
from llm.query_handler import QueryHandler
from llm.utils import parse_arguments
from llm.retriever_manager import RetrieverManager

# Initialize the Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) to allow requests from different domains
CORS(app)

# App configuration settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sql123:password@localhost/passDB'
# Disable modification tracking to save resources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Secret key for sessions, you should change this in a real-world app for security
app.config['SECRET_KEY'] = '12345678'

# Initialize the database and bcrypt for password hashing
db.init_app(app)
bcrypt.init_app(app)

# Initialize components for the chatbot
# Parse arguments to configure the LLM and retriever
args = parse_arguments()

# Create instances of the retriever manager, LLM manager, and query handler
retriever_manager = RetrieverManager()
retriever = retriever_manager.get_retriever()
llm = LLMManager(args).get_llm()
query_handler = QueryHandler(llm, retriever, args)

# Register route to handle user registration
@app.route('/register', methods=['POST'])
def register():
    try:
        # Retrieve user data from request
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # Validate input
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        # Call the function to register the user
        register_user(username, password)
        return jsonify({'message': 'User registered successfully'}), 201
    except ValueError as ve:
        # Handle value errors (e.g., invalid data format)
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        # Handle general exceptions
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

# Register route to handle user login
@app.route('/login', methods=['POST'])
def login():
    try:
        # Retrieve user credentials from request
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # Validate input
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        # Authenticate the user
        if authenticate_user(username, password):
            return jsonify({'message': 'Login successful'}), 200
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        # Handle general exceptions
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

# Register route to handle user logout
@app.route('/logout', methods=['POST'])
def logout():
    try:
        # Call the logout function to terminate the session
        logout_user()
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        # Handle any errors that occur during logout
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

# Register route to handle chatbot interaction
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Check if the user is authenticated before processing the query
        if not is_authenticated():
            return jsonify({'error': 'Unauthorized'}), 401

        # Retrieve the user query from the request
        user_input = request.json.get('query', '').strip()
        if not user_input:
            return jsonify({'error': 'No input provided'}), 400

        # Process the user input through the query handler
        response = query_handler.handle_query(user_input)
        return jsonify({'response': response}), 200
    except Exception as e:
        # Handle any errors during the chat process
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

# Main entry point for the application
if __name__ == "__main__":
    # Create database tables if they don't exist yet
    with app.app_context():
        db.create_all()

    # Run the application in debug mode on localhost at port 5000
    app.run(debug=True, host='127.0.0.1', port=5000)
