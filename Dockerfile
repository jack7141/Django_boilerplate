FROM python:3.11

EXPOSE 8000

WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update \
    && apt-get install -y \
    procps \
    build-essential \
    libpq-dev \
    postgresql-client \
    && apt install git libgeos-dev nginx -y \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]