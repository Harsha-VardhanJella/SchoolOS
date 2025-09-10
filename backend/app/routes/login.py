from fastapi import APIRouter,HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_password,create_access_token,create_refresh_token
from app.db.session import get_db
from app.models.user import User

router = APIRouter(prefix="/login", tags=["login"])
@router.post("/login")