from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Access them using os.getenv
USERNAME = os.getenv("AE_USERNAME")
PASSWORD = os.getenv("AE_PASSWORD")
BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")