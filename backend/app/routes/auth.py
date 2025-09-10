from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password,verify_password,create_access_token,create_refresh_token,decode_token
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


class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == data.email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id), "roles": [user.role]})
    refresh_token = create_refresh_token({"sub": str(user.id),"roles":[user.role]})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

class RefreshRequest(BaseModel):
    refresh_token : str

@router.post("/refresh")
async def Refresh(data: RefreshRequest, db: AsyncSession = Depends(get_db)):

    payload = decode_token(data.refresh_token)
    if "error" in payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Wrong token type")

    user_id = payload.get("sub")
    roles = payload.get("roles", [])

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # 3. Generate new access token with same roles
    access_token = create_access_token({"sub": user_id, "roles": roles})

    return {"access_token": access_token, "token_type": "bearer"}