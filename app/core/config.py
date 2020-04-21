import os
from dotenv import load_dotenv

load_dotenv('.env')

MONGO_CONTAINER = os.getenv("MONGO_CONTAINER")
MONGO_PORT = os.getenv("MONGO_PORT")
DB_NAME = os.getenv("DB_NAME")

# Fetching MongoDB credentials form environment file"
MONGODB_URI = (f"mongodb://{MONGO_CONTAINER}:{MONGO_PORT}/{DB_NAME}")

# Jira credentials

JIRA_URL = os.environ.get('JIRA_URL')
JIRA_USER = os.environ.get('JIRA_USER')
JIRA_PASSWORD = os.environ.get('JIRA_PASSWORD')
