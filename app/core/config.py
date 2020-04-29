import os
from dotenv import load_dotenv

load_dotenv('.env')

# MongoDB Credentials

MONGO_CONTAINER = os.getenv("MONGO_CONTAINER")
MONGO_PORT = os.getenv("MONGO_PORT")
DB_NAME = os.getenv("DB_NAME")
MONGODB_URI = (f"mongodb://{MONGO_CONTAINER}:{MONGO_PORT}/{DB_NAME}")

# Jira credentials

JIRA_URL = os.environ.get('JIRA_URL')
JIRA_USER = os.environ.get('JIRA_USER')
JIRA_PASSWORD = os.environ.get('JIRA_PASSWORD')

# HRMS Credentials

HRMS_USER = os.getenv("HRMS_USER")
ENCRYPTED_PASSWORD = os.getenv("ENCRYPTED_PASS")
LOGIN_URL = os.getenv("LOGIN_URL")
GRAPHQL_URL = os.getenv("GRAPHQL_URL")
