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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Working directory
WORKDIR /app

# Requirements
COPY requirements.txt .

# Install
RUN pip install --no-cache-dir -r requirements.txt

# Code copy
COPY . .

# Port
EXPOSE 8000

# Start
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}