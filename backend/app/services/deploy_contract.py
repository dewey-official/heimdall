import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# RPC 및 계정 정보 설정
w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
private_key = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(private_key)

# ABI와 바이트코드 불러오기
with open("contracts/ChatContract.json") as f:
    contract_data = json.load(f)

abi = contract_data["abi"]
bytecode = contract_data["bytecode"]

# 배포 트랜잭션 생성
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
transaction = contract.constructor().build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 3000000,
    'gasPrice': w3.to_wei('20', 'gwei')
})

# 트랜잭션 서명 및 전송
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# 결과 확인
print("📤 트랜잭션 전송 중... TX Hash:", tx_hash.hex())
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("✅ 배포 완료! 컨트랙트 주소:", receipt.contractAddress)
