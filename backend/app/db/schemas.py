from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# ------------------- User -------------------

class UserBase(BaseModel):
    user_id: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user_id": "0x1234abcd5678efgh"
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

# ------------------- 1. GPT 호출 -------------------

class ChatRequest(BaseModel):
    wallet_address: str
    user_message: str

    class Config:
        json_schema_extra = {
            "example": {
                "wallet_address": "0x1234abcd5678efgh",
                "user_message": "What's a good first date idea?"
            }
        }

class GPTResponse(BaseModel):
    bot_response: str

    class Config:
        json_schema_extra = {
            "example": {
                "bot_response": "Try planning a casual coffee date in a quiet place!"
            }
        }

# ------------------- 2. IPFS 업로드 -------------------

class IPFSUploadRequest(BaseModel):
    wallet_address: str
    user_message: str
    bot_response: str

    class Config:
        json_schema_extra = {
            "example": {
                "wallet_address": "0x1234abcd5678efgh",
                "user_message": "How do I impress on a first date?",
                "bot_response": "Confidence and genuine interest go a long way!"
            }
        }

class IPFSUploadResponse(BaseModel):
    status: str
    ipfs_url: str

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "ipfs_url": "https://gateway.pinata.cloud/ipfs/QmExampleHash"
            }
        }

# ------------------- 3. 온체인 저장 -------------------

class StoreOnChainRequest(BaseModel):
    wallet_address: str
    ipfs_url: str

    class Config:
        json_schema_extra = {
            "example": {
                "wallet_address": "0x1234abcd5678efgh",
                "ipfs_url": "https://gateway.pinata.cloud/ipfs/QmExampleHash"
            }
        }

class StoreOnChainResponse(BaseModel):
    status: str
    tx_hash: str

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "tx_hash": "0xabcdef1234567890"
            }
        }

# ------------------- 4. 히스토리 -------------------

class ChatHistoryRecord(BaseModel):
    ipfs_hash: str
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "ipfs_hash": "https://gateway.pinata.cloud/ipfs/QmExampleHash",
                "created_at": "2025-04-25T12:34:56"
            }
        }

class ChatHistoryResponse(BaseModel):
    user_id: str
    history: List[ChatHistoryRecord]

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "0x1234abcd5678efgh",
                "history": [
                    {
                        "ipfs_hash": "https://gateway.pinata.cloud/ipfs/QmExampleHash",
                        "created_at": "2025-04-25T12:34:56"
                    }
                ]
            }
        }
