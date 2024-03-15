from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# Establish MongoDB connection
def get_db_connection():
    try:
        client = MongoClient(os.environ.get("MONGO_URI"))  
        db = client['GzLLMTest']  # Use the specific database name for this project
        logging.info("Successfully connected to MongoDB")
        return db
    except Exception as e:
        logging.error("Failed to connect to MongoDB: %s", e, exc_info=True)
        return None

def save_user_query(user_query):
    try:
        db = get_db_connection()
        if db is not None:
            collection = db['UserQueries']
            collection.insert_one(user_query)
            logging.info("User query saved successfully.")
        else:
            logging.error("Failed to get database connection for saving user query.")
    except Exception as e:
        logging.error("Failed to save user query: %s", e, exc_info=True)

# Test function to insert and retrieve a document
def test_db_operations():
    try:
        db = get_db_connection()
        if db is not None:
            collection = db['test_collection']
            
            # Insert a test document
            test_document = {"name": "Test User", "message": "Hello, MongoDB!"}
            collection.insert_one(test_document)
            logging.info("Inserted a test document into MongoDB")
            
            # Retrieve the test document
            retrieved_document = collection.find_one({"name": "Test User"})
            logging.info("Retrieved a document: %s", retrieved_document)
    except Exception as e:
        logging.error("Error in test_db_operations: %s", e, exc_info=True)

if __name__ == '__main__':
    test_db_operations()