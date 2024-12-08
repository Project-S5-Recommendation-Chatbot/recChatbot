#!/usr/bin/env python3
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import chatbot components
from llm.llm_manager import LLMManager
from llm.query_handler import QueryHandler
from llm.utils import parse_arguments
from llm.retriever_manager import RetrieverManager
from dbases.Databases import Databases

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Initialize chatbot components
args = parse_arguments()
retriever_manager = RetrieverManager()
retriever = retriever_manager.get_retriever()
llm = LLMManager(args).get_llm()
query_handler = QueryHandler(llm, retriever, args)

@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint to handle user queries and return chatbot responses.
    """
    try:
        # Extract user input from the request body
        user_input = request.json.get('query', '').strip()
        if not user_input:
            return jsonify({'error': 'No input provided'}), 400

        # Process the query using the chatbot's QueryHandler
        response = query_handler.handle_query(user_input)
        # response = "It's working"
        # Return the response as JSON

        return jsonify({'response': response}), 200
        # return response, 200
    except Exception as e:
        # Handle any server-side errors
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
