import os
import json
from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

if not RPC_URL or not PRIVATE_KEY:
    raise EnvironmentError("❌ .env 파일에서 RPC_URL 또는 PRIVATE_KEY가 없습니다.")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SOL 파일과 ABI 출력 경로 설정
SOLIDITY_FILE = os.path.join(BASE_DIR, "..", "contracts", "ChatContract.sol")
ABI_OUTPUT = os.path.join(BASE_DIR, "..", "contracts", "ChatContract.json")

#.env파일
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "..", ".."))  # 예: vahalla 경로

ENV_PATH = os.path.join(PROJECT_ROOT, ".env")


def compile_contract():
    print("📦 컨트랙트 컴파일 중...")

    install_solc("0.8.17")  # 솔리디티 버전 설치

    with open(SOLIDITY_FILE, "r", encoding="utf-8") as f:
        source_code = f.read()

    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "ChatContract.sol": {
                "content": source_code
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "evm.bytecode"]
                }
            }
        }
    }, solc_version="0.8.17")

    # ABI + Bytecode 저장
    with open(ABI_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(compiled_sol, f)

    abi = compiled_sol['contracts']['ChatContract.sol']['ChatContract']['abi']
    bytecode = compiled_sol['contracts']['ChatContract.sol']['ChatContract']['evm']['bytecode']['object']

    print("✅ 컴파일 완료!")
    return abi, bytecode

def deploy_contract(abi, bytecode):
    print("🚀 배포 시작...")

    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    account = w3.eth.account.from_key(PRIVATE_KEY)
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    tx = contract.constructor().build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 3000000,
        'gasPrice': w3.to_wei('25', 'gwei')
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"✅ 배포 완료! 주소: {receipt.contractAddress}")
    return receipt.contractAddress

def update_env(contract_address):
    print("📁 .env 파일에 새 주소 저장 중...")

    if not os.path.exists(ENV_PATH):
        print("⚠️ .env 파일이 존재하지 않습니다. 새로 생성합니다.")
        with open(ENV_PATH, "w", encoding="utf-8") as f:
            f.write(f"CONTRACT_ADDRESS={contract_address}\n")
    else:
        lines = []
        updated = False
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("CONTRACT_ADDRESS="):
                    lines.append(f"CONTRACT_ADDRESS={contract_address}\n")
                    updated = True
                else:
                    lines.append(line)

        if not updated:
            lines.append(f"CONTRACT_ADDRESS={contract_address}\n")

        with open(ENV_PATH, "w", encoding="utf-8") as f:
            f.writelines(lines)

    print("✅ .env 파일 업데이트 완료!")



if __name__ == "__main__":
    abi, bytecode = compile_contract()
    address = deploy_contract(abi, bytecode)
    update_env(address)
