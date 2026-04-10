FROM python:3.11-slim

# System dependencies install karo
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libxcb1 \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

# Working directory set karo
WORKDIR /app

# Requirements copy karo
COPY requirements.txt .

# Libraries install karo
RUN pip install --no-cache-dir -r requirements.txt

# Saara code copy karo
COPY . .

# Port expose karo
EXPOSE 8000

# Server start karo
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}