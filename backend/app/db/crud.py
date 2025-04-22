from sqlalchemy.orm import Session
from . import models, schemas

def create_chat_history(db: Session, chat: schemas.ChatHistoryCreate):
    db_chat = models.ChatHistory(**chat.dict())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def get_chat_histories_by_user(db: Session, user_id: str):
    return db.query(models.ChatHistory).filter(models.ChatHistory.user_id == user_id).all()
