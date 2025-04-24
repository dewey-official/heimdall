### ✅ chat_service.py

from web3 import Web3
import json
import os
from dotenv import load_dotenv
from utils.ipfs import upload_to_ipfs, fetch_from_ipfs
from db import crud, schemas
from sqlalchemy.orm import Session
import openai

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")
openai.api_key = os.getenv("OPENAI_API_KEY")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ABI_OUTPUT = os.path.join(BASE_DIR, "..", "contracts", "ChatContract.json")


with open(ABI_OUTPUT, "r", encoding="utf-8") as f:
    contract_data = json.load(f)
    abi = contract_data["contracts"]["ChatContract.sol"]["ChatContract"]["abi"]

w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)

def ask_gpt(message: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        raise Exception(f"GPT 응답 실패: {str(e)}")

def process_chat_history(user_id: str, user_message: str, bot_response: str, db: Session):
    try:
        data = {"user_message": user_message, "bot_response": bot_response}
        ipfs_url = upload_to_ipfs(data)

        chat_data = schemas.ChatHistoryCreate(user_id=user_id, ipfs_hash=ipfs_url)
        crud.create_chat_history(db, chat_data)

        tx_hash = store_chat_to_chain(user_id, ipfs_url)

        return ipfs_url, tx_hash

    except Exception as e:
        raise Exception(f"Failed to process chat history: {str(e)}")

def store_chat_to_chain(user_address: str, ipfs_url: str) -> str:
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
