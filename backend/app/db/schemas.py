from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

# ------------------- User -------------------

class UserBase(BaseModel):
    user_id: str

    class Config:
        schema_extra = {
            "example": {
                "user_id": "0x1234567890abcdef1234567890abcdef12345678"  # 지갑 주소 예시
            }
        }

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    uuid: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "user_id": "0x1234567890abcdef1234567890abcdef12345678",
                "uuid": "123e4567-e89b-12d3-a456-426614174000",  # UUID 예시
                "created_at": "2025-04-24T12:34:56",  # 예시 날짜
                "updated_at": "2025-04-24T12:34:56",  # 예시 날짜
                "deleted_at": None  # 삭제되지 않은 예시
            }
        }

# ------------------- Chat History -------------------

class ChatHistoryBase(BaseModel):
    user_id: str
    ipfs_hash: str

    class Config:
        schema_extra = {
            "example": {
                "user_id": "0x1234567890abcdef1234567890abcdef12345678",
                "ipfs_hash": "QmZnpv1GnH5G9p8z93ymA3R7Ak94zB7WRXN1cYXhbD5f34"  # 예시 IPFS 해시
            }
        }

class ChatHistoryCreate(ChatHistoryBase):
    pass

class ChatHistoryOut(ChatHistoryBase):
    uuid: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "user_id": "0x1234567890abcdef1234567890abcdef12345678",
                "ipfs_hash": "QmZnpv1GnH5G9p8z93ymA3R7Ak94zB7WRXN1cYXhbD5f34",
                "uuid": "123e4567-e89b-12d3-a456-426614174000",  # UUID 예시
                "created_at": "2025-04-24T12:34:56",  # 예시 날짜
                "updated_at": "2025-04-24T12:34:56",  # 예시 날짜
                "deleted_at": None  # 삭제되지 않은 예시
            }
        }

# ------------------- Chat Process Response -------------------

class ChatProcessResponse(BaseModel):
    status: str
    user_message: str
    bot_response: str
    ipfs_url: str
    tx_hash: str

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "user_message": "Hello, how are you?",
                "bot_response": "I'm doing great, thanks for asking!",
                "ipfs_url": "https://gateway.pinata.cloud/ipfs/QmZnpv1GnH5G9p8z93ymA3R7Ak94zB7WRXN1cYXhbD5f34",
                "tx_hash": "0xabc1234567890abcdef1234567890abcdef1234567890abcdef1234567890ab"  # 예시 트랜잭션 해시
            }
        }
