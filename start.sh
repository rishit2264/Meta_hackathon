#!/bin/bash

echo "===== Application Startup at $(date) ====="

echo "Starting FastAPI Backend..."
python -m uvicorn environment.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

echo "Starting Next.js Frontend..."
cd /app/frontend
PORT=3000 npm start &
FRONTEND_PID=$!
cd /app

# Wait for backend to be ready
echo "Waiting for FastAPI..."
for i in $(seq 1 30); do
    if curl -s http://127.0.0.1:8000/health > /dev/null 2>&1; then
        echo "FastAPI is ready!"
        break
    fi
    sleep 1
done

# Wait for frontend to be ready
echo "Waiting for Next.js..."
for i in $(seq 1 30); do
    if curl -s http://127.0.0.1:3000 > /dev/null 2>&1; then
        echo "Next.js is ready!"
        break
    fi
    sleep 1
done

echo "Starting Nginx on port 7860..."
nginx -c /etc/nginx/nginx.conf
