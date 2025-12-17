# Usamos Python 3.10 slim para manter a imagem o menor possível, mas funcional
FROM python:3.10-slim

# Instala dependências do sistema
# ffmpeg: Obrigatório para extrair áudio de MP4 e converter para MP3
# libmp3lame: Codec necessário para codificação MP3
# git e build-essential: Necessários para compilar algumas libs do Coqui TTS
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libmp3lame0 \
    git \
    build-essential \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/* \
    && ffmpeg -version

WORKDIR /app

# Instala as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte
COPY . .

# Comando padrão para manter o container rodando (ou executar o script)
CMD ["python", "app.py"]