FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY ./app /app/app

# 포트 노출
EXPOSE 8500

# 개발 모드로 실행 (hot reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8500", "--reload"]
