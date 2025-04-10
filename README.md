# Lightweight LLM Chatbot (Local Ollama + Streamlit UI)

A minimal, production-ready chatbot powered by local LLM (e.g., Gemma) using [Ollama](https://ollama.com/) and [Streamlit](https://streamlit.io/).

---

## Features

- Run large language models locally using Ollama
- Interactive UI powered by Streamlit
- Dockerized and ready for deployment
- Automatically pulls model if not yet available

---

## Tech Stack

- Ollama (`gemma3:1b`)
- Streamlit for web interface
- Docker + Docker Compose
- Shell script to bootstrap the model

---

## Project Structure

```
.
├── docker-compose.yml
├── .env
├── ollama
│   ├── dockerfile.ollama
│   └── entrypoint.sh
└── streamlit-ui
    ├── dockerfile.streamlit
    ├── chatbot.py
    └── requirements.txt
```

---

## How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/alfonharyos/docker-llm-chatbot.git
cd docker-llm-chatbot
```

### 2. Create `.env` File

```env
OLLAMA_MODEL=gemma3:1b
```

### 3. Build and Run the Containers

Make sure Docker is installed and running on your system

```bash
docker compose up --build -d
```

### 4. Access the Application

```
http://localhost:8501
```

---

## Supported Models

Use lightweight models compatible with Ollama, such as:

- `gemma:2b`
- `llama2:7b`
- `tinyllama`
- `phi3:mini`

Full model list: [https://ollama.com/library](https://ollama.com/library)

---

## Tips

- Change the model by updating the `OLLAMA_MODEL` value in `.env`
- Make sure your machine has enough resources to run LLMs locally (RAM & CPU)

---



