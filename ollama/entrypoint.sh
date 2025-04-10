#!/bin/sh
set -e

# OLLAMA_MODEL dan OLLAMA_PORT di .env
MODEL_NAME="${OLLAMA_MODEL}"
OLLAMA_PORT="${OLLAMA_PORT}"

echo "Starting temporary Ollama instance to setup model..."
ollama serve &
OLLAMA_PID=$!

# Menunggu hingga Ollama siap menerima koneksi
echo "Waiting for Ollama to be ready on port ${OLLAMA_PORT}..."
until curl -sf http://localhost:$OLLAMA_PORT/; do
  echo "Ollama not ready yet. Retrying in 2s..."
  sleep 2
done

echo "Ollama is ready."

# Cek apakah model sudah di-pull
if ! ollama list | grep -q "$MODEL_NAME"; then
  echo "Pulling model '${MODEL_NAME}'..."
  if ! ollama pull "$MODEL_NAME"; then
    echo "Failed to pull model '${MODEL_NAME}'. Exiting."
    kill "$OLLAMA_PID"
    exit 1
  fi
else
  echo "Model '${MODEL_NAME}' already installed."
fi

# Hentikan instance sementara
echo "Stopping temporary Ollama serve process..."
kill "$OLLAMA_PID"
sleep 2

# Jalankan serve resmi di foreground
echo "Starting Ollama serve in foreground on port ${OLLAMA_PORT}..."
exec ollama serve
