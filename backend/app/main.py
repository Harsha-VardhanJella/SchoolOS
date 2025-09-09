import orjson
from fastapi import FastAPI
from app.core.config import settings
from app.routes import auth 
from app.routes import health as health_routes

def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()

app = FastAPI(title=settings.APP_NAME)

app.include_router(auth.router)

app.include_router(health_routes.router)

@app.get("/")
async def root():
    return {"message": "SchoolOS API up"}


