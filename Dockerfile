FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential curl nodejs npm && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm || true

COPY . .

# Build frontend
WORKDIR /app/frontend
# Ensure package.json exists before npm ci/install
RUN npm install
RUN npm run build
WORKDIR /app

ENV PYTHONPATH=/app PORT=7860 PYTHONUNBUFFERED=1
EXPOSE 7860
HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:7860/health || exit 1
CMD ["uvicorn","environment.main:app","--host","0.0.0.0","--port","7860","--workers","1"]
