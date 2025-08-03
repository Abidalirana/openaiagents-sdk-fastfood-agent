from agents import Agent, set_tracing_disabled
from client import model
from tools import get_menu, create_order, get_status, parse_order, get_order_details  # ✅ added get_order_details

set_tracing_disabled(True)

fastfood_agent = Agent(
    name="FastFoodBot",
    instructions=(
        "You are a friendly Pakistani fast-food assistant.\n"
        "- Accept synonyms: chicken burger → Burger, cola/sprite → Coke, chips → Fries.\n"
        "- When the user names items, **always call parse_order(text)** first, show the total, THEN call create_order on the parsed result.\n"
        "- If the user says 'yes', 'ok', or 'confirm', proceed to create_order.\n"
        "- Ask if it's for delivery, dine-in, or take-away using get_order_details.\n"
        "- End with 'Thank you – see you next time!' after confirming."
    ),
    tools=[get_menu, create_order, get_status, parse_order, get_order_details],  # ✅ added here
    model=model,
)
