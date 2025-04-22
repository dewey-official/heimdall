from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

def create_chat_history(db: Session, chat: schemas.ChatHistoryCreate) -> models.ChatHistory:
    """
    새로운 채팅 기록(IPFS 해시 포함)을 DB에 저장
    """
    db_chat = models.ChatHistory(**chat.dict())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def get_chat_histories_by_user(db: Session, user_id: str) -> List[models.ChatHistory]:
    """
    특정 유저의 모든 채팅 기록을 반환
    """
    return db.query(models.ChatHistory).filter(models.ChatHistory.user_id == user_id).order_by(models.ChatHistory.created_at.desc()).all()

def get_latest_chat_by_user(db: Session, user_id: str) -> Optional[models.ChatHistory]:
    """
    특정 유저의 최신 채팅 기록을 하나 반환
    """
    return db.query(models.ChatHistory).filter(models.ChatHistory.user_id == user_id).order_by(models.ChatHistory.created_at.desc()).first()
