# Docker Setup Explained

This section explains how each Docker-related file contributes to the deployment of the lightweight LLM chatbot system.

---

## `docker-compose.yml`

This file orchestrates two main services:

- `ollama`: a local LLM model server  
- `streamlit-ui`: a simple chat interface

```yaml
version: "3.8"
```

### Services:

#### 1. `ollama`

- **Build**: Uses `dockerfile.ollama` from the `/ollama` directory  
- **Environment Variables**:  
  - `OLLAMA_MODEL`: model to use (e.g., `gemma3:1b`)  
  - `OLLAMA_PORT`: port where Ollama listens (default: `11434`)  
- **Volumes**:  
  - Persists pulled models in `ollama_data`  
- **Networks**:  
  - Connected to internal network `ollama-net`

#### 2. `streamlit-ui`

- **Build**: Uses `dockerfile.streamlit` from the `/streamlit-ui` directory  
- **Ports**:  
  - Exposes port `8501` to access the Streamlit UI  
- **Depends On**:  
  - `ollama` must start first  
- **Env File**:  
  - Reads environment variables from `.env`  
- **Networks**:  
  - Connected to internal `ollama-net`  

```yaml
volumes:
  ollama_data:

networks:
  ollama-net:
    driver: bridge
```

---

## `dockerfile.ollama`

Builds a container that runs the Ollama server and ensures the specified model is pulled before serving.

```dockerfile
FROM ollama/ollama
```

- Uses the official `ollama/ollama` base image, which includes the LLM server.

```dockerfile
RUN apt-get update && apt-get install -y curl && apt-get clean
```

- Installs `curl`, which is needed in the startup script (`entrypoint.sh`) to check if the server is ready (`curl http://localhost:11434`)  
- `apt-get clean` removes cache to reduce image size

```dockerfile
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
```

- Copies the startup script into the container  
- Makes it executable

```dockerfile
ENTRYPOINT ["/entrypoint.sh"]
```

- Ensures the container always starts by running `/entrypoint.sh`

---

## `entrypoint.sh`

This script prepares the model before starting Ollama.

### Why do we need it?

Without this script:

- The Ollama server may start, but the model might not be available yet.
- If a prompt is sent before the model is pulled, it throws `Model not found`.

### What does the script do?

1. **Starts Ollama temporarily in background**  
   - Enables CLI access to pull the model

2. **Waits for Ollama to be ready**  
   - Uses `curl` in a loop to check `http://localhost:11434`

3. **Checks if the model exists**  
   - If not, pulls it with:  
     ```sh
     ollama pull $OLLAMA_MODEL
     ```

4. **Stops the temporary process**  
   - Kills background serve process after pulling

5. **Starts the real Ollama server**  
   - Runs in the foreground and ready to serve requests

---

## `dockerfile.streamlit`

Builds a container for the frontend interface using Streamlit.

```dockerfile
FROM python:3.10-slim
```

- Uses a lightweight Python 3.10 base image

```dockerfile
WORKDIR /app
```

- Sets the working directory inside the container

```dockerfile
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
```

- Installs Python dependencies listed in `requirements.txt`  
- `--no-cache-dir` keeps the image size small

```dockerfile
COPY . .
```

- Copies all app files (like `chatbot.py`) into the container

```dockerfile
CMD ["streamlit", "run", "chatbot.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

- Runs the chatbot app on port `8501`  
- `0.0.0.0` allows external access to the app from the host machine

---

## Summary

| File                   | Purpose                                                  |
|------------------------|----------------------------------------------------------|
| `docker-compose.yml`   | Defines and orchestrates multi-container setup           |
| `dockerfile.ollama`    | Builds a container to serve the LLM with model auto-pull |
| `entrypoint.sh`        | Ensures Ollama and model are ready before serving        |
| `dockerfile.streamlit` | Builds the Streamlit UI to interact with the chatbot     |

---

This setup gives full local control of an LLM-powered chatbot with a user-friendly interface. It’s clean, lightweight, and ready for extension to production environments.

