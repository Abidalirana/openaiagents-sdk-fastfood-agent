from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel
from config import GEMINI_API_KEY, GEMINI_BASE_URL, GEMINI_MODEL

external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=GEMINI_BASE_URL
)

model = OpenAIChatCompletionsModel(
    model=GEMINI_MODEL,
    openai_client=external_client
)