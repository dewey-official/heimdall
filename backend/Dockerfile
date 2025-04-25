FROM python:3.12-slim

WORKDIR /app

# 시스템 패키지 추가
RUN apt-get update && apt-get install -y gcc libffi-dev libssl-dev python3-dev build-essential

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
