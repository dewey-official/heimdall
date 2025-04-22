from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
import datetime

class ChatHistory(Base):
    __tablename__ = "chat_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    ipfs_hash = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
