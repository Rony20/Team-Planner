import os

from dotenv import load_dotenv

load_dotenv('.env')

# Fetching MongoDB credentials form environment file"
MONGODB_URI = os.getenv("MONGODB_URI")

#Jira credentials
JIRA_URL = os.getenv("JIRA_URL")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_PASSWORD = os.getenv("JIRA_PASSWORD")
