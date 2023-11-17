import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESSS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_ACCESS_SECRET = os.getenv("AWS_ACCESS_SECRET")

SRC_PATH = os.getenv("SRC_PATH")
DEST_PATH = os.getenv("DEST_PATH")

# CREATE_USER_URL = os.getenv("CREATE_USER_URL")
# GET_USERS = os.getenv("GET_USERS")
