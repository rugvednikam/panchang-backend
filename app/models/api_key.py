import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Uuid
from sqlalchemy.orm import relationship
from app.models.base import Base

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    hashed_key = Column(String, unique=True, index=True, nullable=False)
    key_prefix = Column(String, nullable=False)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=True) # E.g., 'Production Key'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Simple usage tracking
    total_requests = Column(Integer, default=0)
    
    # Relationship to user
    user = relationship("User", backref="api_keys")
