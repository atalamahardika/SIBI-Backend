FROM python:3.12-slim-bookworm

# Install necessary system dependencies and update all packages
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# Force CPU only + unbuffered logs
ENV CUDA_VISIBLE_DEVICES=""
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--log-level", "debug", "--forwarded-allow-ips", "*"]