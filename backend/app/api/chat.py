from fastapi import APIRouter, HTTPException, Depends, Request, Query
from pydantic import BaseModel
from app.services.chat_service import process_chat_history
from app.services.chat_service import get_chat_history

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


@router.get("/history")
async def get_history(user_id: str = Query(...)):
    """
    해당 user_id에 연결된 IPFS 해시 리스트를 반환합니다.
    """
    return await get_chat_history(user_id)