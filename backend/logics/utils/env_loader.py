import os
from dotenv import load_dotenv, find_dotenv

def load_env():
    dotenv_path = find_dotenv()
    if not dotenv_path:
        raise FileNotFoundError("❌ Could not find .env file.")
    load_dotenv(dotenv_path)
    print(f"✅ .env loaded from: {dotenv_path}")