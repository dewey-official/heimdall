from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.services import chat_service
from app.utils.ipfs import upload_to_ipfs
from app.db import crud, schemas
from app.db.database import get_db

router = APIRouter()

# POST /chat/upload
@router.post("/chat/upload")
def upload_chat(payload: dict, db: Session = Depends(get_db)):
    try:
        user_id = payload.get("wallet_address")
        user_msg = payload.get("user_message")
        bot_msg = payload.get("bot_response")

        if not user_id or not user_msg or not bot_msg:
            raise HTTPException(status_code=400, detail="Missing required fields.")

        # 사용자 없으면 생성
        user = crud.get_user_by_id(db, user_id)
        if not user:
            crud.create_user(db, schemas.UserCreate(user_id=user_id))

        # IPFS 업로드
        data = {
            "user_message": user_msg,
            "bot_response": bot_msg
        }
        ipfs_url = upload_to_ipfs(data)

        # DB 저장
        crud.create_chat_history(db, schemas.ChatHistoryCreate(user_id=user_id, ipfs_hash=ipfs_url))

        # 온체인 저장
        tx_hash = chat_service.store_chat_to_chain(user_id, ipfs_url)

        return {"status": "success", "ipfs_url": ipfs_url, "tx_hash": tx_hash}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# GET /chat/history
@router.get("/chat/history")
def get_history(user_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        return chat_service.get_chat_history(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"History fetch failed: {str(e)}")
