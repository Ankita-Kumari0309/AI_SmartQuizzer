import os
from dotenv import load_dotenv

load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")
MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"

MIN_QUESTIONS = 3
MAX_QUESTIONS = 50