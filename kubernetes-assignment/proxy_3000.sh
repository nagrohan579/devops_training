#!/bin/bash
# Proxy script for port 3000

# Kill any existing processes using these ports
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Start kubectl port-forward for frontend
kubectl port-forward svc/frontend-a-service 3000:3000 &
FRONTEND_PID=$!

# Wait for frontend to start
sleep 2

# Start kubectl port-forward for backend
kubectl port-forward svc/backend 3000:5000 &
BACKEND_PID=$!

echo "Proxies started on port 3000"
echo "Frontend PID: $FRONTEND_PID"
echo "Backend PID: $BACKEND_PID"
echo "Press Ctrl+C to stop"

# Function to clean up when script is terminated
cleanup() {
  echo "Stopping proxies..."
  kill $FRONTEND_PID $BACKEND_PID 2>/dev/null || true
  exit 0
}

# Set up trap to catch signals
trap cleanup SIGINT SIGTERM

# Wait for processes to finish
wait
