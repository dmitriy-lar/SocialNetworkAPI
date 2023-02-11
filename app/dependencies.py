from typing import AsyncGenerator
from .databases import SessionLocal


async def get_db() -> AsyncGenerator:
    """Return async session"""
    async with SessionLocal() as session:
        yield session
