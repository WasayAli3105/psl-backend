FROM python:3.11-slim

# System dependencies install karo
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    libx11-6 \
    libgles2 \
    libegl1 \
    libglvnd0 \
    libglx0 \
    mesa-utils \
    libgles2-mesa \
    && apt-get clean \
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