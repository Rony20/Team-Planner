import os
from dotenv import load_dotenv

load_dotenv('.env')

# MongoDB Credentials

MONGO_CONTAINER = os.getenv("MONGO_CONTAINER")
MONGO_PORT = os.getenv("MONGO_PORT")
DB_NAME = os.getenv("DB_NAME")
# MONGODB_URI = (f"mongodb://{MONGO_CONTAINER}:{MONGO_PORT}/{DB_NAME}")
MONGODB_URI = os.getenv("MONGODB_URI")

# Jira credentials

JIRA_URL = os.getenv('JIRA_URL')
JIRA_USER = os.getenv('JIRA_USER')
JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')

# HRMS Credentials

HRMS_USER = os.getenv("HRMS_USER")
ENCRYPTED_PASSWORD = os.getenv("ENCRYPTED_PASS")
LOGIN_URL = os.getenv("LOGIN_URL")
GRAPHQL_URL = os.getenv("GRAPHQL_URL")

#Active Directory Credentials
AD_HOST = os.getenv("AD_HOST")
AD_PORT = os.getenv("AD_PORT")
AD_URL = f"ldaps://{AD_HOST}:{AD_PORT}"
AD_DOMAIN = os.getenv("AD_DOMAIN")
OU = os.getenv("OU")

#Active Directory Superuser
SUPERUSER_USERNAME = os.getenv('SUPERUSER_USERNAME')
SUPERUSER_PASSWORD = os.getenv('SUPERUSER_PASSWORD')

#JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRES_MINUTES = 480
