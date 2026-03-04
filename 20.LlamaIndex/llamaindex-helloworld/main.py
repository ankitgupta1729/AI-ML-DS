import os
from pathlib import Path

from dotenv import load_dotenv

if __name__ == '__main__':
    env_path = Path(__file__).with_name(".env")
    load_dotenv(dotenv_path=env_path, override=False)
    api_key = os.getenv("OPENAI_API_KEY")

    print("Hello, LlamaIndex!")
    print("Loaded .env from:", env_path)
    print("Your OpenAI API Key is:", os.environ.get("OPENAI_API_KEY"))
