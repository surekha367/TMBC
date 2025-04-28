from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from sqlalchemy.sql import func
from app.config import Base

class MessageLog(Base):
    """
    Database model for tracking WhatsApp message logs
    """
    __tablename__ = "message_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), index=True, nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(20), nullable=False)  # sent, failed, pending
    response_data = Column(Text, nullable=True)  # Store API response as JSON string
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Create indexes for common queries
    __table_args__ = (
        Index('idx_message_logs_status_created', status, created_at),
    )

    def __repr__(self):
        return f"<MessageLog(id={self.id}, phone_number={self.phone_number}, status={self.status})>"