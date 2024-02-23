# Use a imagem oficial do Ubuntu como imagem base
FROM ubuntu:latest

# Configure o diretório de trabalho
WORKDIR /app

# Atualize os pacotes e instale as dependências
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    python3.11-venv \
    poppler-utils \
    ttf-mscorefonts-installer \
    && rm -rf /var/lib/apt/lists/*

# Copie o arquivo de requisitos para o diretório de trabalho


# Crie e ative a virtualenv
RUN python3.11 -m venv venv
RUN . venv/bin/activate

# Instale as dependências do pip
#RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos do aplicativo para o diretório de trabalho
COPY . .

# Comando padrão para iniciar o aplicativo quando o contêiner for iniciado
CMD ["python3", "appy.py"]
