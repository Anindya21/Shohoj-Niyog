import os
from dotenv import load_dotenv, find_dotenv

def load_env():
    dotenv_path = find_dotenv()
    if dotenv_path:
        load_dotenv(dotenv_path)
        print(f"✅ .env loaded from: {dotenv_path}")
    else:
        # In Docker or prod: rely on environment variables already provided
        print("ℹ️ No .env file found, using system environment variables instead.")
