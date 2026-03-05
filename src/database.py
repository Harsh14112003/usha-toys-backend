import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_DETAILS = os.getenv("DB_CONNECTION_STRING")

if not MONGO_DETAILS:
    raise ValueError("DB_CONNECTION_STRING is not set in environment variables")

client = MongoClient(MONGO_DETAILS)

database = client.get_database("usa-toys") # Default database name, can be changed

def get_db():
    return database
