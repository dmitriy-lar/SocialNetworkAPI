from .databases import AsyncSession, SessionLocal


async def get_db() -> AsyncSession:
    """Return async session"""
    async with SessionLocal() as session:
        yield session
