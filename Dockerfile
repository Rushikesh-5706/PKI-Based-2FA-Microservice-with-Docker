FROM python:3.11-slim as builder
WORKDIR /app
RUN pip install --user --no-cache-dir fastapi uvicorn cryptography pyotp requests python-multipart

FROM python:3.11-slim
WORKDIR /app
ENV TZ=UTC
ENV PATH=/root/.local/bin:$PATH
RUN apt-get update && apt-get install -y cron tzdata && rm -rf /var/lib/apt/lists/*
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY --from=builder /root/.local /root/.local
COPY . .
RUN chmod 0644 /app/cron/2fa-cron && crontab /app/cron/2fa-cron && mkdir -p /data /cron
EXPOSE 8080
CMD cron && uvicorn app.main:app --host 0.0.0.0 --port 8080
