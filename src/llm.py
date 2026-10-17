import os

from dotenv import load_dotenv
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model=os.environ["MODEL_NAME"],
    timeout=30,
    max_retries=2,
)
