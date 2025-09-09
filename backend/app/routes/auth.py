from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password
from app.db.session import get_db
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name:str
    role:str

@router.post("/register")
async def register(payload: UserRegister, db: AsyncSession = Depends(get_db)):
    if len(payload.password) < 8:
        raise HTTPException(status_code=400, detail="Password too short")

    # check existing user
    stmt = select(User).where(User.email == payload.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    # create new user
    hashed = hash_password(payload.password)
    user = User(email=payload.email, password_hash=hashed,name=payload.name,role=payload.role)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {"id": user.id, "email": user.email}
