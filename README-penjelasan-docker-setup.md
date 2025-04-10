# Penjelasan Setup Docker

Bagian ini menjelaskan bagaimana setiap file terkait Docker berkontribusi dalam proses deployment sistem chatbot LLM ringan.

---

## `docker-compose.yml`

File ini mengatur dua layanan utama:

- `ollama`: server model LLM lokal  
- `streamlit-ui`: antarmuka obrolan sederhana

```yaml
version: "3.8"
```

### Services:

#### 1. `ollama`

- **Build**: Menggunakan `dockerfile.ollama` dari direktori `/ollama`  
- **Environment Variables**:  
  - `OLLAMA_MODEL`: model yang digunakan (contoh: `gemma3:1b`)  
  - `OLLAMA_PORT`: port tempat Ollama mendengarkan (default: `11434`)  
- **Volumes**:  
  - Menyimpan model yang sudah ditarik dalam `ollama_data`  
- **Networks**:  
  - Terhubung ke jaringan internal `ollama-net`

#### 2. `streamlit-ui`

- **Build**: Menggunakan `dockerfile.streamlit` dari direktori `/streamlit-ui`  
- **Ports**:  
  - Mengekspos port `8501` untuk mengakses UI Streamlit  
- **Depends On**:  
  - `ollama` harus dijalankan terlebih dahulu  
- **Env File**:  
  - Membaca variabel lingkungan dari `.env`  
- **Networks**:  
  - Terhubung ke `ollama-net`  

```yaml
volumes:
  ollama_data:

networks:
  ollama-net:
    driver: bridge
```

---

## `dockerfile.ollama`

Membangun container yang menjalankan server Ollama dan memastikan model yang ditentukan sudah tersedia sebelum melayani permintaan.

```dockerfile
FROM ollama/ollama
```

- Menggunakan image dasar resmi `ollama/ollama` yang sudah menyertakan server LLM.

```dockerfile
RUN apt-get update && apt-get install -y curl && apt-get clean
```

- Menginstal `curl`, yang diperlukan dalam skrip startup (`entrypoint.sh`) untuk memeriksa apakah server sudah siap (`curl http://localhost:11434`)  
- `apt-get clean` membersihkan cache untuk memperkecil ukuran image

```dockerfile
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
```

- Menyalin skrip startup ke dalam container  
- Memberi izin eksekusi

```dockerfile
ENTRYPOINT ["/entrypoint.sh"]
```

- Memastikan container selalu memulai dengan menjalankan `/entrypoint.sh`

---

## `entrypoint.sh`

Skrip ini menyiapkan model sebelum menjalankan Ollama.

### Mengapa skrip ini dibutuhkan?

Tanpa skrip ini:

- Server Ollama bisa saja sudah berjalan, tetapi modelnya belum tersedia.
- Jika permintaan dikirim sebelum model ditarik, akan terjadi error `Model not found`.

### Apa yang dilakukan oleh skrip ini?

1. **Menjalankan Ollama sementara di background**  
   - Untuk memungkinkan akses CLI dan menarik model

2. **Menunggu hingga Ollama siap**  
   - Menggunakan `curl` dalam loop untuk memeriksa `http://localhost:11434`

3. **Memeriksa apakah model sudah ada**  
   - Jika belum, menarik model dengan:  
     ```sh
     ollama pull $OLLAMA_MODEL
     ```

4. **Menghentikan proses sementara**  
   - Menghentikan serve sementara setelah model tersedia

5. **Menjalankan Ollama sesungguhnya**  
   - Berjalan di foreground dan siap melayani permintaan

---

## `dockerfile.streamlit`

Membangun container untuk antarmuka frontend menggunakan Streamlit.

```dockerfile
FROM python:3.10-slim
```

- Menggunakan image Python 3.10 yang ringan

```dockerfile
WORKDIR /app
```

- Menetapkan direktori kerja di dalam container

```dockerfile
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
```

- Menginstal dependensi Python dari `requirements.txt`  
- `--no-cache-dir` menjaga ukuran image tetap kecil

```dockerfile
COPY . .
```

- Menyalin semua file aplikasi (seperti `chatbot.py`) ke dalam container

```dockerfile
CMD ["streamlit", "run", "chatbot.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

- Menjalankan aplikasi chatbot di port `8501`  
- `0.0.0.0` memungkinkan akses dari luar container

---

## Ringkasan

| File                  | Tujuan                                                        |
|-----------------------|---------------------------------------------------------------|
| `docker-compose.yml`  | Mendefinisikan dan mengatur setup multi-container             |
| `dockerfile.ollama`   | Membangun container untuk LLM dengan auto-pull model          |
| `entrypoint.sh`       | Memastikan Ollama dan model siap sebelum melayani permintaan  |
| `dockerfile.streamlit`| Membangun UI Streamlit untuk berinteraksi dengan chatbot      |

---

Setup ini memberikan kontrol penuh untuk menjalankan chatbot berbasis LLM secara lokal dengan antarmuka yang ramah pengguna. Desainnya ringan, bersih, dan mudah diperluas ke lingkungan produksi.

