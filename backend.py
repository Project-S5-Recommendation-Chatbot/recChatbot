#!/usr/bin/env python3
import os
import sys

from flask import Flask, request, jsonify
from flask_cors import CORS

from authentication import db, bcrypt, authenticate_user, logout_user
from dbases.Databases import Databases  # Importing the Databases class
from ingestor.document_ingestion import DocumentIngestion
from ingestor.vectorstore import VectorStoreHandler
from llm.llm_manager import LLMManager
from llm.query_handler import QueryHandler
from llm.retriever_manager import RetrieverManager
from llm.utils import parse_arguments

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
databases = Databases()
# Parse arguments to configure LLM and retriever
args = parse_arguments()

# Create instances of LLM manager, retriever manager, and query handler
retriever_manager = RetrieverManager()
retriever = retriever_manager.get_retriever()
llm = LLMManager(args).get_llm()
query_handler = QueryHandler(llm, retriever, args)
# Ingestion inits
source_directory = os.getenv("SOURCE_DIRECTORY", "source_documents")
persist_directory = os.getenv("PERSIST_DIRECTORY")
embeddings_model_name = os.getenv("EMBEDDINGS_MODEL_NAME")
chunk_size = int(os.getenv("CHUNK_SIZE", 500))
chunk_overlap = int(os.getenv("CHUNK_OVERLAP", 50))


def ingest_data(source_directory, persist_directory, embeddings_model_name, chunk_size, chunk_overlap):
    vectorstore = VectorStoreHandler(persist_directory, embeddings_model_name)
    ingestion = DocumentIngestion(source_directory, chunk_size, chunk_overlap)

    if vectorstore.does_vectorstore_exist():
        documents = ingestion.process_documents()
        db = vectorstore.get_vectorstore()
        db.add_documents(documents)
    else:
        documents = ingestion.process_documents()
        vectorstore.create_vectorstore(documents)


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
        # Get the user query from request
        user_input = request.json.get('query', '').strip()
        if not user_input:
            return jsonify({'error': 'No input provided'}), 400
        if user_input == "exit":
            response = jsonify({'success': 'Exited Successfully'})
            response.status_code = 200
            print(response.get_json())  # Optional: Log the response before exiting
            sys.exit(0)  # Exits the program
        databases.fetch_data_based_on_prompt(user_input)
        ingest_data(source_directory, persist_directory, embeddings_model_name, chunk_size, chunk_overlap)
        # Pass the modified query to the chatbot's query handler
        response = query_handler.handle_query(f"{user_input}")
        # f" at French University in Armenia")
        # Convert stop words to lowercase
        stop_words = [
            "i don't know", "i'm just telling you", "don't", "note:", "(note:)", "answer", "unhelpful",
            "i", "useless", "note", "not-so-helpful", "not", "helpful", "limitation", "limitations",
            "seems", "please", "unfortunately", "fortunately", "unfortunately,", "fortunately,",
            "however", "however,", "since", "since,", "{", "}", "source", "source,", "source:",
            "question", "question", "question:", "question:"
        ]

        stop_words = [word.lower() for word in stop_words]  # Convert to lowercase

        response2 = ""

        # Split the response into words
        words = response.split()

        # Iterate over words and append to response2 until a stop word is encountered
        for word in words:
            if word.lower() in stop_words:  # Check if the lowercase version of the word is in stop words
                break
            response2 += word + " "

        # Trim any trailing whitespace from response2
        response2 = response2.strip()
        response2 += "."

        return jsonify({'response': response2}), 200
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
    databases.close_connections()
