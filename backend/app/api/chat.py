from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from services import chat_service
from utils.ipfs import upload_to_ipfs
from db import crud, schemas
from db.database import get_db
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

# ------------------- 1. GPT 호출만 수행 -------------------
@router.post("/chat/ask", response_model=schemas.GPTResponse)
def ask_bot(payload: schemas.ChatRequest):
    """
    GPT를 호출하여 사용자 메시지에 대한 응답을 생성한다.
    """
    try:
        user_msg = payload.user_message
        logger.debug(f"GPT ask request: {user_msg}")

        if not user_msg:
            raise HTTPException(status_code=400, detail="User message is required.")

        bot_msg = chat_service.ask_gpt(user_msg)
        return schemas.GPTResponse(bot_response=bot_msg)

    except Exception as e:
        logger.error(f"GPT ask failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"GPT ask failed: {str(e)}")

# ------------------- 2. IPFS 업로드만 수행 -------------------
@router.post("/chat/upload_ipfs", response_model=schemas.IPFSUploadResponse)
def upload_to_ipfs_only(payload: schemas.IPFSUploadRequest):
    """
    유저/봇 대화 데이터를 IPFS에 업로드하고 해당 URL을 반환한다.
    """
    try:
        data = {
            "user_message": payload.user_message,
            "bot_response": payload.bot_response
        }
        ipfs_url = upload_to_ipfs(data)
        return schemas.IPFSUploadResponse(status="success", ipfs_url=ipfs_url)

    except Exception as e:
        logger.error(f"IPFS upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"IPFS upload failed: {str(e)}")

# ------------------- 3. IPFS 해시 온체인 저장 -------------------
@router.post("/chat/store", response_model=schemas.StoreOnChainResponse)
def store_on_chain(payload: schemas.StoreOnChainRequest):
    """
    IPFS URL을 블록체인 스마트컨트랙트에 저장하고 트랜잭션 해시를 반환한다.
    """
    try:
        user_id = payload.wallet_address
        ipfs_url = payload.ipfs_url

        if not user_id or not ipfs_url:
            raise HTTPException(status_code=400, detail="Missing required fields.")

        tx_hash = chat_service.store_chat_to_chain(user_id, ipfs_url)
        return schemas.StoreOnChainResponse(status="success", tx_hash=tx_hash)

    except Exception as e:
        logger.error(f"On-chain store failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"On-chain store failed: {str(e)}")

# ------------------- 4. 유저별 채팅 히스토리 조회 -------------------
@router.get("/chat/history", response_model=schemas.ChatHistoryResponse)
def get_history(user_id: str = Query(...), db: Session = Depends(get_db)):
    """
    유저 주소를 기반으로 IPFS 기반의 채팅 히스토리 목록을 조회한다.
    """
    try:
        return chat_service.get_chat_history(db, user_id)
    except Exception as e:
        logger.error(f"History fetch failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"History fetch failed: {str(e)}")
