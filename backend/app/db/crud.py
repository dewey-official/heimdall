from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db import models, schemas

# -------------------- User --------------------

def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(user_id=user.user_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# -------------------- Chat History --------------------

def create_chat_history(db: Session, chat: schemas.ChatHistoryRecord):
    db_chat = models.ChatHistory(user_id=chat.user_id, ipfs_hash=chat.ipfs_hash)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def get_chat_histories_by_user(db: Session, user_id: str):
    return (
        db.query(models.ChatHistory)
        .filter(models.ChatHistory.user_id == user_id)
        .order_by(models.ChatHistory.created_at.desc())
        .all()
    )
