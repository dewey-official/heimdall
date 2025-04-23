import requests
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

# --- 환경 변수 로딩 ---
PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY")
PINATA_URL = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

if not PINATA_API_KEY or not PINATA_SECRET_API_KEY:
    raise EnvironmentError("❌ Pinata API 키가 .env 파일에 설정되지 않았습니다.")

def upload_to_ipfs(data: Dict[str, Any]) -> str:
    """
    JSON 데이터를 Pinata에 업로드하고, IPFS 게이트웨이 URL을 반환합니다.
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

    try:
        response = requests.post(PINATA_URL, json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"❌ IPFS 업로드 실패: {str(e)}")

    ipfs_hash = response.json().get("IpfsHash")
    if not ipfs_hash:
        raise ValueError("❌ 응답에서 IPFS 해시를 찾을 수 없습니다.")

    return f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"


def fetch_from_ipfs(ipfs_url: str) -> Dict[str, Any]:
    """
    IPFS 게이트웨이 URL로부터 JSON 데이터를 불러옵니다.
    """
    try:
        response = requests.get(ipfs_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise Exception(f"❌ IPFS에서 데이터를 불러오는 중 오류 발생: {str(e)}")
