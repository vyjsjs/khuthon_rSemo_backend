FROM python:3.12-slim

WORKDIR /app

# 필요한 시스템 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 사용하는 프레임워크에 맞게 CMD 수정 필요 (아래는 FastAPI uvicorn 예시)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]