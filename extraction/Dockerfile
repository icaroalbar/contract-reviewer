# Imagem base
FROM python:3.11-slim

# Evita prompts interativos durante instalações
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependências do sistema para OCR e PDFs
RUN apt-get update && apt-get install -y \
    git \
    tesseract-ocr \
    tesseract-ocr-por \
    poppler-utils \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho
WORKDIR /app

# Copia requirements.txt e instala Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto
COPY . .

# Comando padrão
CMD ["python", "handler.py"]
