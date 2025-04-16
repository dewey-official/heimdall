from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

# 환경 변수 로드
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")  # 서버에 보관된 관리자용 키
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")  # 해당 키의 지갑 주소

# ABI 로드
with open("app/contracts/abi.json") as f:
    abi = json.load(f)

# Web3 인스턴스 생성
w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)

def store_chat_to_chain(user_address: str, ipfs_url: str) -> str:
    """
    스마트 컨트랙트에 채팅 기록(IPFS 링크)를 저장하는 함수
    """
    nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS)

    txn = contract.functions.storeChat(user_address, ipfs_url).build_transaction({
        'from': PUBLIC_ADDRESS,
        'nonce': nonce,
        'gas': 200000,
        'gasPrice': w3.to_wei('30', 'gwei')
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    return w3.to_hex(tx_hash)
