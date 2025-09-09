import enum, uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class Role(str, enum.Enum):
    Admin = "Admin"
    Teacher = "Teacher"
    Student = "Student"

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    password_hash: Mapped[str] = mapped_column(String(255))
    # Using a portable (non-native) enum type for easy edits during dev
    role: Mapped[Role] = mapped_column(Enum(Role, name="role_enum", native_enum=False))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
