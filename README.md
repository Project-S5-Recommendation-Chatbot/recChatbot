---

# **Recommendation Chatbot for the French University in Armenia**

This project is an **AI-powered Recommendation Chatbot** designed to streamline communication and enhance information management at the **French University in Armenia**. By addressing fragmented communication and multilingual challenges, this chatbot improves operational efficiency and user satisfaction through centralized data access, real-time updates, and multilingual support.

---

## **Table of Contents**

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [System Architecture](#system-architecture)
5. [Installation Guide](#installation-guide)
6. [Usage Instructions](#usage-instructions)
7. [API Endpoints](#api-endpoints)
8. [Project Structure](#project-structure)
9. [Configuration and Environment Variables](#configuration-and-environment-variables)
10. [Contributing](#contributing)
11. [Future Plans](#future-plans)
12. [License](#license)

---

## **Project Overview**

The **Recommendation Chatbot** is an innovative AI-driven solution developed to improve the management of educational resources at the **French University in Armenia**. The chatbot serves several purposes:
- **Multilingual Communication**: It supports multiple languages, enabling seamless interaction between the university’s multilingual community (students, faculty, and staff).
- **Centralized Information Access**: Users can interact with the system to get up-to-date information about university regulations, academic requirements, courses, and more.
- **AI-Powered Recommendations**: The chatbot makes intelligent recommendations based on user queries, helping users find information more efficiently.
- **Real-Time Data Updates**: Integrated with the university’s databases to ensure that users always get the latest information.

This system is part of a broader initiative to modernize communication within educational institutions and pave the way for future innovation in AI-based educational tools.

---

## **Features**

- **User Authentication and Authorization**:  
   - Secure user registration, login, and logout functionalities.
   - Session management with encrypted credentials using `bcrypt`.

- **Multilingual Support**:  
   - The chatbot can respond to queries in multiple languages, making it adaptable to the diverse linguistic needs of users.

- **Real-Time Data Access**:  
   - Centralized database for all university-related data, ensuring up-to-date and consistent information across various departments.

- **AI-Powered Query Handling**:  
   - Uses **Large Language Models (LLMs)** for intelligent, natural language processing to handle user queries.
   - Advanced retrieval logic for querying specific information from the database or documents.

- **Chatbot Interface**:  
   - Users interact with the system via a simple API endpoint that processes queries and returns contextually relevant responses.

---

## **Technologies Used**

- **Backend Framework**:  
   - **Flask** (Python) for building the web application and handling HTTP requests.

- **Database**:  
   - **PostgreSQL** and **MongoDB** for storing user data and university information (SQLAlchemy ORM for interaction with the database).

- **AI Components**:  
   - Custom **LLM Manager**, **Retriever Manager**, and **Query Handler** for processing user queries intelligently.
   - Natural Language Processing (NLP) techniques for multilingual support.

- **Authentication**:  
   - **bcrypt** for secure password hashing and authentication.

- **Environment Management**:  
   - **Python-dotenv** for managing environment variables and sensitive credentials.

- **Web Security**:  
   - **Flask-CORS** for handling Cross-Origin Resource Sharing (CORS) in API calls.

- **Deployment**:  
   - Local development setup with Flask’s built-in server.

---

## **System Architecture**

### **High-Level Overview:**
- **Backend**: The backend consists of a Flask application serving API endpoints, integrated with PostgreSQL for database management, and leveraging AI components to process and respond to user queries.
- **AI System**: The AI system is based on a combination of **Large Language Models (LLMs)** for intelligent query interpretation, and a **Retriever Manager** for accessing the most relevant data.

**Diagram Overview (for visualization):**

1. **User Interaction** (via API)
2. **Flask Backend** (handles routing, user requests, and responses)
3. **Database** (PostgreSQL stores data such as university regulations and user credentials)
4. **AI Models** (Large Language Models and Retrieval Logic for processing and responding to queries)

---

## **Installation Guide**

### **Prerequisites:**
Before setting up the project, ensure you have the following installed:
- Python 3.9 or above
- PostgreSQL Database
- `git` for cloning the repository
- Virtual environment tools (`venv` or `conda`)

### **Steps to Install:**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/<your-username>/recommendation-chatbot.git
   cd recommendation-chatbot
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Project Dependencies:**
   Install all the necessary Python libraries from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database:**
   - Make sure you have **PostgreSQL** installed and configured.
   - Create a new database called `passDB`.
   - Update the database connection URI in `backend.py` or `.env` file:
     ```bash
     DATABASE_URI=postgresql://<username>:<password>@localhost/passDB
     ```

5. **Run Database Migrations:**
   Initialize the database tables by running:
   ```bash
   python backend.py
   ```

6. **Start the Flask Application:**
   - Run the application locally in development mode:
   ```bash
   python backend.py
   ```

7. **Access the Application:**
   - Once running, access the API via `http://127.0.0.1:5000` from your browser or API testing tool like Postman.

---

## **Usage Instructions**

Once the server is up and running, you can interact with the chatbot through the provided API endpoints.

### **API Endpoints:**

1. **User Registration:**  
   - `POST /register`  
   **Body:**  
   ```json
   {
     "username": "example_user",
     "password": "example_password"
   }
   ```

2. **User Login:**  
   - `POST /login`  
   **Body:**  
   ```json
   {
     "username": "example_user",
     "password": "example_password"
   }
   ```

3. **User Logout:**  
   - `POST /logout`

4. **Chatbot Query:**  
   - `POST /chat`  
   **Body:**  
   ```json
   {
     "query": "What are the admission requirements for this semester?"
   }
   ```

   - **Response:**
   ```json
   {
     "response": "The admission requirements are..."
   }
   ```

---

---

## **Configuration and Environment Variables**

Create a `.env` file to manage sensitive information and configuration settings:
```
DATABASE_URI=postgresql://<username>:<password>@localhost/passDB
SECRET_KEY=<your_secret_key>
```

---

## **Contributing**

We welcome contributions! If you would like to contribute to the development of this chatbot:
1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to your forked repository (`git push origin feature-branch`).
5. Open a Pull Request.

---

## **Future Plans**

- **Advanced AI Models**: Integration of more advanced AI models for better user experience and deeper context understanding.
- **Cloud Deployment**: Host the application on a cloud platform (e.g., AWS, Heroku) for scalability.
- **User Analytics**: Implement analytics to track and improve chatbot performance and user interaction.

---
Feel free to reach out if you have any questions, suggestions, or contributions to make!
