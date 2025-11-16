import os
from dotenv import load_dotenv

load_dotenv() 

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
DATABASE_URL = os.getenv("DATABASE_URL")
