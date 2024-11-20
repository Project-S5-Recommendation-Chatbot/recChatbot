from src.ConnectionMongoDB import ConnectionMongoDB
from src.ConnectionMySqlDB import ConnectionMySqlDB
from src.keywords import keywords
from src.mongoconfig import mongo_config
from src.mysqlconfig import mysql_config
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class Databases:

    def __init__(self):
        self.mongo_conn = ConnectionMongoDB(self.mongo_config["uri"])
        self.mongo_client = self.mongo_conn.connect()

        self.mysql_conn = ConnectionMySqlDB(**self.mysql_config)
        self.mysql_connection = self.mysql_conn.connect()

        nltk.download('stopwords')
        nltk.download('punkt')

    def get_all_mysql_rows(self, table_name):  # TO EDIT TABLE NAMES
        with self.mysql_connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            return cursor.fetchall()

    def get_all_documents(self, db_name, collection_name):
        database = self.mongo_client[db_name]
        collection = database[collection_name]
        return list(collection.find())

    def students(self):
        return self.get_all_mysql_rows("students_table")  # TO EDIT TABLE NAMES

    def exams(self):
        return self.get_all_documents("certification_exams_db", "exams_collection")

    def exchanges(self):
        return self.get_all_documents("exchange_programs_db", "exchanges_collection")

    def internships(self):
        return self.get_all_documents("job_internship_db", "internships_collection")

    def regulations(self):
        return self.get_all_documents("university_regulations_db", "regulations_collection")

    def fetch_data_based_on_prompt(self, user_prompt):

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
            if best_match == "students":
                return self.students()
            elif best_match == "exams":
                return self.exams()
            elif best_match == "exchanges":
                return self.exchanges()
            elif best_match == "internships":
                return self.internships()
            elif best_match == "regulations":
                return self.regulations()
        else:
            raise ValueError("No matching category found in the prompt!")

    def close_mongo_connection(self):
        self.mongo_conn.close()

    def close_mysql_connection(self):
        self.mysql_conn.close()
