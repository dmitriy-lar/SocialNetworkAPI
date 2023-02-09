import uvicorn
from fastapi import FastAPI
from .settings import INIT_TABLES, DEBUG
from .databases import engine, Base
from .routers import users

if DEBUG:
    app = FastAPI(title="Social Network API", version="1.0.0")
else:
    app = FastAPI(title="Social Network API", version="1.0.0", redoc_url=None, docs_url=None)

"""Include routers"""
app.include_router(users.router)
""""""


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # if INIT_TABLES=True -> create new empty tables
        if INIT_TABLES:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        else:
            await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    uvicorn.run(app=app, host='127.0.0.1', port=8000)
