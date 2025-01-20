from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Groq configuration for the Llama model
GROQ_CONFIG = [
    {
        "model": "llama3-70b-8192",  # Llama model
        "api_key": os.getenv("GROQ_API_KEY"),  # Fetch API key from .env
        "api_type": "groq",  # Specify Groq as the API type
        "temperature": 0.5,
        # "max_tokens": 2048,
        # "top_p": 0.9,
        # "frequency_penalty": 0.0,
        # "presence_penalty": 0.0,
    }
]
