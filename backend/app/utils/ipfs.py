import requests
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY")
PINATA_URL = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

def upload_to_ipfs(data: Dict[str, Any]) -> str:
    """
    JSON 데이터를 IPFS에 업로드하고 CID 해시를 반환합니다.
    """
    headers = {
        "Content-Type": "application/json",
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }

    payload = {
        "pinataOptions": {"cidVersion": 1},
        "pinataContent": data
    }

    response = requests.post(PINATA_URL, json=payload, headers=headers)

    if response.status_code == 200:
        ipfs_hash = response.json()["IpfsHash"]
        return f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
    else:
        raise Exception(f"IPFS 업로드 실패: {response.text}")
