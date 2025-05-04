#!/bin/bash
# Proxy script for port 3001

# Kill any existing processes using these ports
lsof -ti:3001 | xargs kill -9 2>/dev/null || true

# Start kubectl port-forward for frontend
kubectl port-forward svc/frontend-b-service 3001:3000 &
FRONTEND_PID=$!

# Wait for frontend to start
sleep 2

# Start kubectl port-forward for backend
kubectl port-forward svc/backend 3001:5000 &
BACKEND_PID=$!

echo "Proxies started on port 3001"
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
