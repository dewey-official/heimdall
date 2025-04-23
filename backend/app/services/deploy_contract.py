import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# --- 환경 변수 로드 ---
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

if not RPC_URL or not PRIVATE_KEY:
    raise EnvironmentError("❌ .env 파일에서 RPC_URL 또는 PRIVATE_KEY를 찾을 수 없습니다.")

# --- Web3 인스턴스 및 계정 세팅 ---
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

# --- ABI 및 Bytecode 불러오기 ---
ABI_PATH = "app/contracts/ChatContract.json"
if not os.path.exists(ABI_PATH):
    raise FileNotFoundError(f"❌ ABI 파일을 찾을 수 없습니다: {ABI_PATH}")

with open(ABI_PATH, "r") as f:
    contract_data = json.load(f)

abi = contract_data.get("abi")
bytecode = contract_data.get("bytecode")

if not abi or not bytecode:
    raise ValueError("❌ ABI 또는 Bytecode가 유효하지 않습니다.")

# --- 컨트랙트 인스턴스 및 배포 트랜잭션 생성 ---
contract = w3.eth.contract(abi=abi, bytecode=bytecode)

print("📦 스마트 컨트랙트 배포 시작...")

transaction = contract.constructor().build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 3_000_000,
    'gasPrice': w3.to_wei('25', 'gwei')
})

# --- 서명 및 트랜잭션 전송 ---
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

print(f"📤 트랜잭션 전송 중... TX Hash: {tx_hash.hex()}")

receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# --- 결과 출력 ---
print("✅ 배포 완료!")
print(f"🔗 컨트랙트 주소: {receipt.contractAddress}")
