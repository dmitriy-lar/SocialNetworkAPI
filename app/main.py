import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Social Network API", redoc_url=None, version="1.0.0")


@app.get('/')
async def main_root() -> dict:
    return {'message': 'Main Root'}


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8000)
