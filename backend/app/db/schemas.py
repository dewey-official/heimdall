from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

# ------------------- User -------------------

class UserBase(BaseModel):
    user_id: str

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    uuid: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# ------------------- Chat History -------------------

class ChatHistoryBase(BaseModel):
    user_id: str
    ipfs_hash: str

class ChatHistoryCreate(ChatHistoryBase):
    pass

class ChatHistoryOut(ChatHistoryBase):
    uuid: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True
