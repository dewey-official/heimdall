from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from services import chat_service
from utils.ipfs import upload_to_ipfs
from db import crud, schemas
from db.database import get_db

router = APIRouter()

# POST /chat/process
@router.post("/chat/process", response_model=schemas.ChatProcessResponse)
def process_chat(payload: dict, db: Session = Depends(get_db)):
    try:
        # 요청에서 user_id와 user_msg 추출
        user_id = payload.get("wallet_address")
        user_msg = payload.get("user_message")

        # 필드 확인
        if not user_id or not user_msg:
            raise HTTPException(status_code=400, detail="Missing required fields.")

        # 사용자 확인 및 생성
        user = crud.get_user_by_id(db, user_id)
        if not user:
            crud.create_user(db, schemas.UserCreate(user_id=user_id))

        # GPT 응답 받기
        bot_msg = chat_service.ask_gpt(user_msg)

        # 채팅 기록을 IPFS에 업로드하고 URL을 받음
        ipfs_url, tx_hash = chat_service.process_chat_history(user_id, user_msg, bot_msg, db)

        # 응답 반환
        return schemas.ChatProcessResponse(
            status="success",
            user_message=user_msg,
            bot_response=bot_msg,
            ipfs_url=ipfs_url,
            tx_hash=tx_hash
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")


# POST /chat/upload
@router.post("/chat/upload", response_model=schemas.ChatProcessResponse)
def upload_chat(payload: dict, db: Session = Depends(get_db)):
    try:
        # 요청에서 user_id, user_msg, bot_msg 추출
        user_id = payload.get("wallet_address")
        user_msg = payload.get("user_message")
        bot_msg = payload.get("bot_response")

        # 필드 확인
        if not user_id or not user_msg or not bot_msg:
            raise HTTPException(status_code=400, detail="Missing required fields.")

        # 사용자 확인 및 생성
        user = crud.get_user_by_id(db, user_id)
        if not user:
            crud.create_user(db, schemas.UserCreate(user_id=user_id))

        # 메시지를 IPFS에 업로드
        data = {"user_message": user_msg, "bot_response": bot_msg}
        ipfs_url = upload_to_ipfs(data)

        # 채팅 기록 데이터베이스에 저장
        crud.create_chat_history(db, schemas.ChatHistoryCreate(user_id=user_id, ipfs_hash=ipfs_url))

        # 블록체인에 채팅 저장 후 트랜잭션 해시 받기
        tx_hash = chat_service.store_chat_to_chain(user_id, ipfs_url)

        # 응답 반환
        return schemas.ChatProcessResponse(
            status="success",
            user_message=user_msg,
            bot_response=bot_msg,
            ipfs_url=ipfs_url,
            tx_hash=tx_hash
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# GET /chat/history
@router.get("/chat/history")
def get_history(user_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        # 사용자 ID에 대한 채팅 기록 반환
        return chat_service.get_chat_history(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"History fetch failed: {str(e)}")
