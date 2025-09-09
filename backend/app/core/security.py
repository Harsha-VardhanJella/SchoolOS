import bcrypt
from jose import jwt 
from datetime import datetime,timedelta,timezone
from app.core.config import settings

def hash_password(password:str):
    return bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")
def verify_password(password:str,truehashpass:bytes):
    return bcrypt.checkpw(password.encode("utf-8"),truehashpass.encode("utf-8"))

SECRET_KEY=settings.JWT_SECRET
ALGO="HS256"

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc) +timedelta(minutes=settings.JWT_EXPIRES_MINUTES)
    to_encode.update({"exp":expire,"type":"access"})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGO)

def create_refresh_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc) +timedelta(minutes=settings.JWT_EXPIRES_REFRESH)
    to_encode.update({"exp":expire,"type":"refresh"})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGO)

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
    except Exception as e:
        return {"error": str(e)}
