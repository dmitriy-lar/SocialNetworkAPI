from .settings import config_env
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

DATABASE_URL = f"postgresql+asyncpg://{config_env.get('POSTGRES_USER')}:{config_env.get('POSTGRES_PASSWORD')}@localhost/{config_env.get('POSTGRES_NAME')}"

engine = create_async_engine(url=DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()
