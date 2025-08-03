from pydantic import BaseModel
from agents import function_tool

# ---------- Menu ----------
class MenuOut(BaseModel):
    Burger: int
    Fries: int
    Coke: int
    Deal: int

@function_tool
def get_menu() -> MenuOut:
    """Return the fast-food menu."""
    return MenuOut(Burger=300, Fries=150, Coke=100, Deal=500)

# ---------- Order ----------
class OrderIn(BaseModel):
    Burger: int = 0
    Fries: int = 0
    Coke: int = 0
    Deal: int = 0

@function_tool
def create_order(order: OrderIn) -> str:
    """Create a new order."""
    total = (
        order.Burger * 300
        + order.Fries * 150
        + order.Coke * 100
        + order.Deal * 500
    )
    ordered = {k: v for k, v in order.dict().items() if v}
    return (
        f"✅ Order confirmed: {ordered}. "
        f"Total: {total} PKR. "
        f"Estimated delivery: 20 minutes. "
        f"Thank you – see you next time!"
    )

# ---------- Smart parser ----------
@function_tool
def parse_order(text: str) -> OrderIn:
    """
    Parse free-text order like 'one burger two cokes' into OrderIn.
    Returns 0 for anything not mentioned.
    """
    text = text.lower()
    counts = {"burger": 0, "fries": 0, "coke": 0, "deal": 0}
    synonyms = {
        "burger": {"burger", "chicken burger"},
        "fries": {"fries", "chips"},
        "coke": {"coke", "cola", "sprite", "pepsi"},
        "deal": {"deal", "combo"},
    }

    # simple word-to-number map
    numbers = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
    }

    words = text.split()
    for i, w in enumerate(words):
        for key, aliases in synonyms.items():
            if w in aliases:
                # look one word back for quantity
                qty = 1
                if i > 0 and words[i - 1] in numbers:
                    qty = numbers[words[i - 1]]
                counts[key] += qty

    return OrderIn(
        Burger=counts["burger"],
        Fries=counts["fries"],
        Coke=counts["coke"],
        Deal=counts["deal"],
    )

# ---------- Status ----------
@function_tool
def get_status(order_id: str) -> str:
    return f"🕒 Order {order_id} is being prepared!"
#==============================================
# ---------- Order Details (Fallback Info) ----------
class OrderDetails(BaseModel):
    order_type: str  # delivery, dine-in, take-away
    phone: str = ""
    address: str = ""

@function_tool
def get_order_details(details: OrderDetails) -> str:
    """
    Collects order type and optional delivery details.

    Args:
        order_type: delivery, dine-in, or take-away.
        phone: (optional) phone number for delivery.
        address: (optional) address for delivery.

    Returns:
        A confirmation message.
    """
    order_type = details.order_type.lower()
    if order_type == "delivery":
        return (
            f"🛵 Your order will be delivered to {details.address}. "
            f"We may contact you at {details.phone}. Thank you!"
        )
    elif order_type == "dine-in":
        return "🍽️ Your dine-in order is confirmed. We look forward to serving you!"
    elif order_type == "take-away":
        return "🥡 Your take-away order is confirmed. It’ll be ready soon!"
    else:
        return "❌ Invalid order type. Please choose delivery, dine-in, or take-away."
