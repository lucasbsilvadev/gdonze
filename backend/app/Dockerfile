FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# dependências para weasyprint e fontes
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    fontconfig \
    fonts-liberation \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# garantindo estrutura de pastas 
RUN mkdir -p templates/html templates/propostas output

COPY . .

# garantindo permissões de escrita na pasta de saída para o weasyprint
RUN chmod -R 777 /app/output

EXPOSE 8000

# cmd para prod
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]