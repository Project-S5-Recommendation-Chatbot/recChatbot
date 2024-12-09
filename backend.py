#!/usr/bin/env python3
import os
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from authentication import db, bcrypt, register_user, authenticate_user, logout_user, is_authenticated
from llm.llm_manager import LLMManager
from llm.query_handler import QueryHandler
from llm.utils import parse_arguments
from llm.retriever_manager import RetrieverManager

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# App configuration settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Ensure session works properly

# Initialize database and bcrypt
db.init_app(app)
bcrypt.init_app(app)

# Parse arguments to configure LLM and retriever
args = parse_arguments()

# Create instances of LLM manager, retriever manager, and query handler
retriever_manager = RetrieverManager()
retriever = retriever_manager.get_retriever()
llm = LLMManager(args).get_llm()
query_handler = QueryHandler(llm, retriever, args)

# Route to handle user login
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        if authenticate_user(username, password):
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route to handle user logout
@app.route('/logout', methods=['POST'])
def logout():
    try:
        logout_user()
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500


# Route to handle chatbot interactions
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Ensure the user is authenticated
        # if not is_authenticated():
        #     return jsonify({'error': 'Unauthorized'}), 401

        # Get the user query from request
        user_input = request.json.get('query', '').strip()
        if not user_input:
            return jsonify({'error': 'No input provided'}), 400
        ingest_data(source_directory, persist_directory, embeddings_model_name, chunk_size, chunk_overlap)
        # Pass the query to the chatbot's query handler
        response = query_handler.handle_query(user_input)
        return jsonify({'response': response}), 200
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500


# Main application entry
if __name__ == "__main__":
    # Ensure database tables are created before the server runs
    with app.app_context():
        db.create_all()
        print("Database initialized!")

    # Start the server
    app.run(debug=True, host='127.0.0.1', port=5000)
