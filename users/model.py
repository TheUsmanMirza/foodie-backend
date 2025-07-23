import uuid
import enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, Boolean, Enum
from database import Base
from datetime import datetime


class Tier(enum.Enum):
    FREE = "FREE"
    PREMIUM = "PREMIUM"


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(BaseModel):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    name = Column(String)
    password = Column(String)
    is_verified = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    tier = Column(Enum(Tier), default=Tier.FREE, nullable=False)
    restaurant_id = Column(UUID(as_uuid=True), default=None)

