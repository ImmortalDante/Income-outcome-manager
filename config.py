from dotenv import load_dotenv
import os


load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")
