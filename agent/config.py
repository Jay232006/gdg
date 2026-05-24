import os
from dotenv import load_dotenv

# Load environment variables from backend or root directory if present
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
PORT = int(os.getenv("PORT", "8000"))
DB_URL = os.getenv("DB_URL", "sqlite:///./crickhealth.db")
