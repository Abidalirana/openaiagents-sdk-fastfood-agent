Below is a clean, fully-modular version of the same bot split into logical files that can live in the same folder (or be packaged later).
Copy each block into its own file and run python main.py to start chatting.
📁 requirements.txt
Text
Copy
openai-agents==0.1.0   # or the exact version you have
python-dotenv
📁 .env
bash
Copy
GEMINI_API_KEY=your_real_key_here
📁 config.py
Python
Copy
import os
from dotenv import load_dotenv

# Load once, expose everywhere
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is missing in .env")

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
GEMINI_MODEL = "gemini-2.0-flash"
📁 client.py
Python
Copy
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
📁 tools.py
Python
Copy
from agents import function_tool

@function_tool
def get_menu() -> dict:
    """Return the fast-food menu."""
    return {
        "Burger": 300,
        "Fries": 150,
        "Coke": 100,
        "Deal": 500,
    }

@function_tool
def create_order(order: dict) -> str:
    """Create a new order (mock)."""
    return f"✅ Order received: {order}. Estimated delivery: 20 minutes."

@function_tool
def get_status(order_id: str) -> str:
    """Return order status (mock)."""
    return f"🕒 Order {order_id} is being prepared!"
📁 agent.py
Python
Copy
from agents import Agent, set_tracing_disabled
from client import model
from tools import get_menu, create_order, get_status

set_tracing_disabled(True)

fastfood_agent = Agent(
    name="FastFoodBot",
    instructions=(
        "You are a smart fast-food order assistant. "
        "Help customers browse the menu, place orders, and check status."
    ),
    tools=[get_menu, create_order, get_status],
    model=model
)
📁 main.py
Python
Copy
import asyncio
from agents import Runner
from agent import fastfood_agent

async def main() -> None:
    user_input = input("🍔 You: ")
    result = await Runner.run(fastfood_agent, user_input)
    print(f"🤖 Bot: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
✅ Quick Start
bash
Copy
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
Enjoy your modular fast-food bot!
Copy
Retry
Share
How do I set up the .env file?

Can I customize the menu items?

What's the purpose of the 'set_tracing_disabled' function?