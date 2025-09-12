import orjson
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 🔹 import CORS
from app.core.config import settings
from app.routes import auth 
from app.routes import health as health_routes

def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()

app = FastAPI(title=settings.APP_NAME)

# 🔹 Add CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGINS],  # e.g., "http://localhost:5173"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(health_routes.router)

@app.get("/")
async def root():
    return {"message": "SchoolOS API up"}
