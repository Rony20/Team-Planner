import os

from dotenv import load_dotenv

load_dotenv('.env')

# Ftaching MongoDB credentials form environment file"
MONGODB_URI = os.getenv("MONGODB_URI")
