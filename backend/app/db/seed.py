# app/db/seed.py
import asyncio
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.user import User, Role
from app.core.security import hash_password

USERS = [
    {"email": "admin@schoolos.com",  "name": "Admin", "role": Role.Admin,   "password": "pass1234"},
    {"email": "teacher@schoolos.com","name": "Harsha", "role": Role.Teacher, "password": "pass1234"},
    {"email": "student@schoolos.com","name": "Bannu",      "role": Role.Student, "password": "pass1234"},
]

async def run():
    async with AsyncSessionLocal() as session:
        for u in USERS:
            exists = (await session.execute(select(User).where(User.email == u["email"]))).scalar_one_or_none()
            if exists:
                continue
            session.add(User(
                email=u["email"],
                name=u["name"],
                role=u["role"],
                password_hash=hash_password(u["password"]),
            ))
        await session.commit()

if __name__ == "__main__":
    asyncio.run(run())
