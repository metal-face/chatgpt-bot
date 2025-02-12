from openai import OpenAI
from settings import OPENAI_API_KEY

client = OpenAI(
    api_key=OPENAI_API_KEY,
)
