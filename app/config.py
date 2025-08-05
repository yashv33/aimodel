from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.local")  # Ensure correct .env file is loaded

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

settings = Settings()
