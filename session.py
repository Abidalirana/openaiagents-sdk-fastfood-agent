from __future__ import annotations

import json
from typing import List, Dict, Any
import asyncpg
from agents import Session

class PostgreSQLSession(Session):
    """
    PostgreSQL-backed session for openai-agents.
    Keeps the entire conversation history as JSONB.
    """

    _pool: asyncpg.Pool | None = None

    def __init__(self, session_id: str) -> None:
        super().__init__(session_id)
        # Direct connection string, no .env needed
        self.conn_str = "postgresql://postgres:admin@localhost:5432/fastfood"

    # --- pool helper ---
    async def _pool(self) -> asyncpg.Pool:
        if PostgreSQLSession._pool is None:
            PostgreSQLSession._pool = await asyncpg.create_pool(
                self.conn_str, min_size=1, max_size=10
            )
        return PostgreSQLSession._pool

    # --- Session API ---
    async def get(self) -> List[Dict[str, Any]]:
        pool = await self._pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT messages FROM agent_sessions WHERE session_id = $1",
                self.session_id,
            )
            return json.loads(row["messages"]) if row else []

    async def set(self, messages: List[Dict[str, Any]]) -> None:
        pool = await self._pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO agent_sessions (session_id, messages)
                VALUES ($1, $2)
                ON CONFLICT (session_id) DO UPDATE
                SET messages = EXCLUDED.messages
                """,
                self.session_id,
                json.dumps(messages),
            )

    async def delete(self) -> None:
        pool = await self._pool()
        async with pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM agent_sessions WHERE session_id = $1",
                self.session_id,
            )
