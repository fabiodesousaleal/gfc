# 1 INTRODUÇÃO
    Esse sistema gera uma ficha catalográfica com dados de entrada do usuário
## 2 REQUERIMENTOS
    2.1 Python
    2.2 Reportlab
    2.3 pacote de fontes msttcorefonts
    2.4 Flask
    2.4.1 Flask-login
    2.5 pdf2image
    2.6 poppler
    2.7 Make
    2.8 python-dotenv

## 3 SUBINDO COM DOCKER   
    1 - clonar o projeto
    2 - make up  

### 3.1 Acessando
    localhost:5000

## 4 INSTALAÇÃO MANUAL
### 4.1 msttcorefonts    
    echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | sudo debconf-set-selections
    echo ttf-mscorefonts-installer msttcorefonts/present-mscorefonts-eula note | sudo debconf-set-selections
    sudo apt-get install ttf-mscorefonts-installer --quiet --assume-yes   
### 4.2 flask  
    pip install flask
### 4.3 pdf2image
    pip install pdf2image
### 4.4 poppler
    pip install poppler-utils
### 4.5 Iniciar o flask
    python3 app.py
### 4.6 ACESSANDO
    localhost:5000

## 5 VERSÕES 
    - Versão 1.0.0 : Projeto Inicial
    - Versão 1.0.1 : Altera logo, e layout do app

## 6 DETALHES
    - Usar o comando make help para ver as opções disponiveis
    _ criar o arquivo .env com a SECRET_KEY