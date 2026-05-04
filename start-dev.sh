#!/bin/bash
# Start all services for local development
# Usage: ./start-dev.sh

set -e

echo "=== Starting Paoding MVP (dev mode) ==="

# Start Java service
echo "[1/3] Starting Java service on port 8080..."
cd paoding-java
if [ ! -f target/paoding-java-1.0.0-SNAPSHOT.jar ]; then
    echo "Building Java service..."
    mvn clean package -q -DskipTests
fi
java -jar target/paoding-java-1.0.0-SNAPSHOT.jar &
JAVA_PID=$!
cd ..

# Wait for Java to start
echo "Waiting for Java service to be ready..."
for i in $(seq 1 30); do
    if curl -s http://localhost:8080/api/v1/hotel/search -X POST \
        -H "Content-Type: application/json" \
        -d '{"arrCity":"test"}' > /dev/null 2>&1; then
        echo "Java service is ready!"
        break
    fi
    sleep 1
done

# Start Python service
echo "[2/3] Starting Python service on port 8000..."
cd paoding-python
if [ ! -d .venv ]; then
    echo "Creating Python virtual environment..."
    python -m venv .venv
    .venv/bin/pip install -q .
fi
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
PYTHON_PID=$!
cd ..

# Start Vue dev server
echo "[3/3] Starting Vue dev server on port 5173..."
cd paoding-web
if [ ! -d node_modules ]; then
    echo "Installing npm dependencies..."
    npm install
fi
npx vite --host &
VUE_PID=$!
cd ..

echo ""
echo "=== All services started! ==="
echo "  Java API:    http://localhost:8080"
echo "  Python API:  http://localhost:8000"
echo "  Vue App:     http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all services"

# Trap Ctrl+C
trap "echo 'Stopping services...'; kill $JAVA_PID $PYTHON_PID $VUE_PID 2>/dev/null; exit 0" INT TERM

wait
