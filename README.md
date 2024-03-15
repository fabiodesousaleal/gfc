# 1 INTRODUÇÃO
    Esse sistema gera uma ficha catalográfica com dados de entrada do usuário, foi desenvolvido em python, usando o framework flask.


## 2 SUBINDO COM DOCKER   
    Esse projeto conta com o automatizador Make, portanto tenha ele instalado para poder executar os passos abaixo.
    
    1 - Clonar o projeto gfc
    2 - make up
    3 - Após o comando acima, será solicitado no terminal o nome  de usuario e posteriormente a senha, esse será o usuário a ser utilizado pelo sistema para gerenciar os parametros da ficha.
    4 - Para ver outras opções utilize o comando "make help"
    5 - Por padrão a aplicação estará disponivel em localhost:5000

## 3 INSTALAÇÃO MANUAL -  REQUERIMENTOS
    3.1 Python
    3.2 Reportlab
    3.3 pacote de fontes msttcorefonts
    3.4 Flask
    3.4.1 Flask-login
    3.5 pdf2image
    3.6 poppler
    3.7 Make
    3.8 python-dotenv

### 4.1 msttcorefonts  (PACOTE DE FONTES)  
    echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | sudo debconf-set-selections
    echo ttf-mscorefonts-installer msttcorefonts/present-mscorefonts-eula note | sudo debconf-set-selections
    sudo apt-get install ttf-mscorefonts-installer --quiet --assume-yes   
### 4.2 flask  (FRAMEWORK)
    pip install flask
### 4.3 pdf2image (LIB PARA GERAR PDF)
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