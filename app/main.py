from fastapi import FastAPI
from app.routers.users import router as user_router
from app.routers.clients import router as client_router
app = FastAPI()


@app.get('/hello')
async def hello():
    return {'Message': 'Hello world'}

app.include_router(user_router)
app.include_router(client_router)
