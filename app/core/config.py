import os

from dotenv import load_dotenv

load_dotenv('.env')

# MongoDB Credentials

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")

# Fetching MongoDB credentials form environment file"

MONGODB_URI = (f"mongodb://{MONGO_USER}"
               f":{os.environ['MONGO_PASSWORD']}@{os.environ['MONGO_HOST']}"
               f":{os.environ['MONGO_PORT']}")

# Jira credentials

JIRA_URL = os.getenv('JIRA_URL')
JIRA_USER = os.getenv('JIRA_USER')
JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')

# HRMS Credentials

HRMS_USER = os.getenv("HRMS_USER")
ENCRYPTED_PASSWORD = os.getenv("ENCRYPTED_PASS")
LOGIN_URL = os.getenv("LOGIN_URL")
GRAPHQL_URL = os.getenv("GRAPHQL_URL")
