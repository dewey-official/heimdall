from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from app.services.chat_service import process_chat_history

router = APIRouter()

class ChatHistoryPayload(BaseModel):
    wallet_address: str
    user_message: str
    bot_response: str

@router.post("/chat/upload")
async def upload_chat(payload: ChatHistoryPayload):
    try:
        ipfs_hash = process_chat_history(
            wallet_address=payload.wallet_address,
            user_message=payload.user_message,
            bot_response=payload.bot_response
        )
        return {"status": "success", "ipfs_hash": ipfs_hash}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
