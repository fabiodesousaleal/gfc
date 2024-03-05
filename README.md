# 1 INTRODUÇÃO
    Esse sistema gera uma ficha catalográfica com dados de entrada do usuário
## 2 REQUERIMENTOS
    2.1 Python
    2.2 Reportlab
    2.3 pacote de fontes msttcorefonts
    2.4 Flask
    2.5 pdf2image
    2.6 poppler
    2.7 Make
## 3 INSTALAÇÃO no linux/ubuntu
### 3.1 - msttcorefonts    
    echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | sudo debconf-set-selections
    echo ttf-mscorefonts-installer msttcorefonts/present-mscorefonts-eula note | sudo debconf-set-selections
    sudo apt-get install ttf-mscorefonts-installer --quiet --assume-yes   
### 3.2 - flask  
    pip install flask
### 3.3 - pdf2image
    pip install pdf2image
### 3.4 - poppler
    pip install poppler-utils
## 4 - Iniciar o flask
    python3 app.py

# 5 - ACESSANDO
    localhost:5000

# 6 - SUBINDO COM DOCKER   
    clone do projeto
    make up   

# 7 - ACESSANDO
    localhost:5000

# 8 - USUÁRIO PADRÃO
    username: admin
    password: admin

## 9 - VERSÕES
    - Versão 1.0.0 : Projeto Inicial

## 10 - EXTRAS
    - alterar a senha de login no arquivo e executa novamente o migrate:
        /migrations/1_inicial.py 
    

