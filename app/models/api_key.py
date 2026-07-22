import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Uuid
from sqlalchemy.orm import relationship
from app.models.base import Base

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=True) # E.g., 'Production Key'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Simple usage tracking
    total_requests = Column(Integer, default=0)
    
    # Relationship to user
    user = relationship("User", backref="api_keys")
