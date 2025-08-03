import asyncio
import uuid
import asyncpg
import json
from agents import Runner
from agent import fastfood_agent

# ✅ Fixed PostgreSQL connection string
DB_URL = "postgresql://postgres:admin@localhost:5432/fastfood"

async def save_convo(session_id: str, messages: list):
    async with asyncpg.create_pool(DB_URL) as pool:
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO agent_sessions (session_id, messages)
                VALUES ($1, $2)
                ON CONFLICT (session_id) DO UPDATE
                SET messages = EXCLUDED.messages
                """,
                session_id,
                json.dumps(messages),
            )

async def load_convo(session_id: str) -> list:
    async with asyncpg.create_pool(DB_URL) as pool:
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT messages FROM agent_sessions WHERE session_id = $1",
                session_id,
            )
            return json.loads(row["messages"]) if row else []

async def main():
    print("🍔 FastFoodBot ready! Type 'quit' to exit.\n")
    session_id = str(uuid.uuid4())
    history = await load_convo(session_id)

    # Initial system prompt if no history
    if not history:
        history = [
            {
                "role": "system",
                "content": (
                    "You are a friendly Pakistani fast-food assistant. "
                    "Accept synonyms like chicken burger→Burger, cola→Coke. "
                    "Show total price before confirming."
                ),
            }
        ]

    while True:
        user_input = input("🍔 You: ").strip()
        if user_input.lower() in {"quit", "exit"}:
            print("👋 Goodbye!")
            break

        history.append({"role": "user", "content": user_input})
        result = await Runner.run(fastfood_agent, history)
        print(f"🤖 Bot: {result.final_output}")
        history.append({"role": "assistant", "content": result.final_output})
        await save_convo(session_id, history)

if __name__ == "__main__":
    asyncio.run(main())
