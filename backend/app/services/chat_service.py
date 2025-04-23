from web3 import Web3
import json
import os
from dotenv import load_dotenv
from app.utils.ipfs import upload_to_ipfs, fetch_from_ipfs
from app.db import crud, schemas
from sqlalchemy.orm import Session

load_dotenv()

# 환경 변수 로드
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")

# ABI 로드
with open("app/contracts/abi.json") as f:
    abi = json.load(f)

# Web3 인스턴스 생성
w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)


def process_chat_history(user_id: str, user_message: str, bot_response: str, db: Session):
    """
    사용자 채팅 데이터를 IPFS에 저장하고, IPFS 해시를 DB와 온체인에 저장
    """
    try:
        # IPFS에 채팅 데이터 업로드
        data = {
            "user_message": user_message,
            "bot_response": bot_response
        }
        ipfs_url = upload_to_ipfs(data)

        # DB에 채팅 기록 저장
        chat_data = schemas.ChatHistoryCreate(user_id=user_id, ipfs_hash=ipfs_url)
        crud.create_chat_history(db, chat_data)

        # 온체인에 채팅 기록 저장
        tx_hash = store_chat_to_chain(user_id, ipfs_url)

        return ipfs_url

    except Exception as e:
        raise Exception(f"Failed to process chat history: {str(e)}")


def store_chat_to_chain(user_address: str, ipfs_url: str) -> str:
    """
    스마트 컨트랙트에 채팅 기록(IPFS 링크)을 저장
    """
    try:
        nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS)

        txn = contract.functions.storeChat(ipfs_url).build_transaction({
            'from': PUBLIC_ADDRESS,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': w3.to_wei('30', 'gwei')
        })

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return w3.to_hex(tx_hash)

    except Exception as e:
        raise Exception(f"Failed to store chat to chain: {str(e)}")


def get_chat_history(db: Session, user_id: str):
    """
    DB에서 user_id의 IPFS 해시 리스트를 가져오고 IPFS에서 내용을 조회해 반환
    """
    try:
        chat_records = crud.get_chat_histories_by_user(db, user_id)
    except Exception as e:
        raise Exception(f"❌ DB 조회 중 오류: {str(e)}")

    chat_contents = []
    for record in chat_records:
        try:
            content = fetch_from_ipfs(record.ipfs_hash)
            chat_contents.append({
                "hash": record.ipfs_hash,
                "content": content,
                "timestamp": record.created_at.isoformat() if record.created_at else None
            })
        except Exception as e:
            chat_contents.append({
                "hash": record.ipfs_hash,
                "error": f"IPFS fetch error: {str(e)}"
            })

    return {
        "user_id": user_id,
        "chats": chat_contents
    }
