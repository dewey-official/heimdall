from pydantic import BaseModel
from datetime import datetime

class ChatHistoryCreate(BaseModel):
    user_id: str
    ipfs_hash: str

class ChatHistoryOut(BaseModel):
    id: int
    user_id: str
    ipfs_hash: str
    created_at: datetime

    class Config:
        orm_mode = True
