# Use uma imagem Debian/Ubuntu com Python 3.11
FROM python:3.11-slim

# Evita prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependências do sistema para OCR e PDFs
RUN apt-get update && apt-get install -y \
    git \
    tesseract-ocr \
    tesseract-ocr-por \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho
WORKDIR /app

# Copia requirements e instala pacotes Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da função Lambda
COPY . .

# Instala AWS Lambda Runtime Interface Emulator para testar localmente
RUN pip install --no-cache-dir awslambdaric

# Entry point para Lambda
ENTRYPOINT ["/usr/local/bin/python3", "-m", "awslambdaric"]

# Comando padrão: aponta para a função Lambda
CMD ["handler.lambda_handler"]
