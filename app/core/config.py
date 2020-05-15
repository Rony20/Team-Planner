import os

from dotenv import load_dotenv

load_dotenv(".env")

# MongoDB Credentials

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")

# Fetching MongoDB credentials form environment file"

MONGODB_URI = (f"mongodb://{MONGO_USER}"
               f":{MONGO_PASSWORD}@{MONGO_HOST}"
               f":{MONGO_PORT}")

# Jira credentials

JIRA_URL = os.getenv("JIRA_URL")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_PASSWORD = os.getenv("JIRA_PASSWORD")

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
SUPERUSER_USERNAME = os.getenv("SUPERUSER_USERNAME")
SUPERUSER_PASSWORD = os.getenv("SUPERUSER_PASSWORD")

#JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRES_MINUTES = 480
