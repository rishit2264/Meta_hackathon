FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential curl nodejs npm && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV PYTHONPATH=/app PORT=7860 PYTHONUNBUFFERED=1
EXPOSE 7860
HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:7860/health || exit 1
CMD ["uvicorn","environment.main:app","--host","0.0.0.0","--port","7860","--workers","1"]
