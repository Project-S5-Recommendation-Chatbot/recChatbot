import json  # For working with JSON data
import os  # For file and directory operations
from datetime import date  # For handling dates
from decimal import Decimal  # For working with decimal numbers

import nltk  # For Natural Language Processing tasks
from nltk.corpus import stopwords  # To remove common words in NLP
from nltk.tokenize import word_tokenize  # To tokenize text into words

from dbases.ConnectionMongoDB import ConnectionMongoDB  # MongoDB connection module
from dbases.ConnectionPostgreSQLDB import ConnectionPostgreSQLDB  # PostgreSQL connection module
from dbases.keywords import keywords  # Dictionary of keywords for matching
from dbases.mongoconfig import mongo_config  # MongoDB configuration
from dbases.postgresqlconfig import postgresql_config  # PostgreSQL configuration
from dbases.tables import tables  # List of PostgreSQL tables to fetch data from


# Class to manage interactions with both MongoDB and PostgreSQL databases
class Databases:
    def __init__(self):
        # Initialize connections to MongoDB and PostgreSQL
        self.mongo_conn = ConnectionMongoDB(mongo_config["uri"])
        self.mongo_client = self.mongo_conn.connect()

        self.postgres_conn = ConnectionPostgreSQLDB(**postgresql_config)
        self.postgres_connection = self.postgres_conn.connect()

        # Download necessary NLTK datasets
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)

        # Ensure the directory for storing source documents exists
        self._ensure_directory("../source_documents")

    def _ensure_directory(self, path):
        """Ensure the directory exists."""
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    def _write_to_file(self, filename, data):
        """Helper function to write data as plain text to a file in ../source_documents."""
        file_path = os.path.join("../source_documents", f"{filename}.txt")

        def format_data(obj, level=0):
            """Recursively format data as text with proper indentation."""
            indent = "    " * level
            if isinstance(obj, dict):
                return "\n".join(
                    f"{indent}{key}: {format_data(value, level + 1)}" for key, value in obj.items()
                )
            elif isinstance(obj, list):
                return "\n".join(f"{indent}- {format_data(item, level + 1)}" for item in obj)
            elif isinstance(obj, Decimal):
                return str(float(obj))
            elif isinstance(obj, date):
                return obj.isoformat()
            else:
                return f"{obj}"

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(format_data(data))

    def get_all_postgres_rows(self):
        """Fetches all rows from PostgreSQL tables and writes to a file."""
        all_data = {}

        with self.postgres_connection.cursor() as cursor:
            for table in tables:
                try:
                    cursor.execute(f"SELECT * FROM {table}")
                    rows = cursor.fetchall()
                    all_data[table] = rows
                except Exception as e:
                    print(f"Error fetching data from table '{table}': {e}")

        self._write_to_file("postgres_all_data", all_data)
        return all_data

    def get_all_documents(self, db_name, collection_name):
        """Fetches all documents from a MongoDB collection and writes to a file."""
        database = self.mongo_client[db_name]
        collection = database[collection_name]
        data = list(collection.find())
        self._write_to_file(f"mongo_{db_name}_{collection_name}", data)
        return data

    def fetch_category_data(self, category):
        """Fetches data for a specific category."""
        category_methods = {
            "students": self.get_all_postgres_rows,
            "exams": lambda: self.get_all_documents("Chatbot", "Exam_FCE"),
            "regulations": lambda: self.get_all_documents("university_regulations_db", "regulations_collection"),
        }

        if category not in category_methods:
            raise ValueError(f"Unknown category: {category}")

        return category_methods[category]()

    def fetch_data_based_on_prompt(self, user_prompt):
        """Fetches data based on user prompt."""
        stop_words = set(stopwords.words('english'))
        prompt_words = word_tokenize(user_prompt.lower())
        cleaned_prompt = [word for word in prompt_words if word not in stop_words]

        cleaned_prompt_text = " ".join(cleaned_prompt)

        match_counts = {category: 0 for category in keywords}
        for category, words in keywords.items():
            for keyword in words:
                if keyword in cleaned_prompt_text:
                    match_counts[category] += 1

        best_match = max(match_counts, key=match_counts.get)
        if match_counts[best_match] > 0:
            return self.fetch_category_data(best_match)
        else:
            raise ValueError("No matching category found in the prompt!")

    def close_connections(self):
        """Closes the MongoDB and PostgreSQL connections."""
        self.mongo_conn.close()
        self.postgres_conn.close()
