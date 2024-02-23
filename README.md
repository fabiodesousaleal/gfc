#REQUERIMENTOS
    ## 1 INTRODUÇÃO
        Esse sistema gera uma ficha catalográfica com dados de entrada do usuário
    ## 2 REQUERIMENTOS
        ### 2.1 Python
        ### 2.2 Reportlab
        ### 2.3 pacote de fontes msttcorefonts
        ### 2.4 Flask
        ### 2.5 pdf2image
        ### 2.6 
    ## 3 INSTALAÇÃO no linux/ubuntu
        ## 3.1 - msttcorefonts
        ```bash
        echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | sudo debconf-set-selections
        echo ttf-mscorefonts-installer msttcorefonts/present-mscorefonts-eula note | sudo debconf-set-selections
        sudo apt-get install ttf-mscorefonts-installer --quiet --assume-yes
        ```
        ## 3.2 - flask
        ```bash
            pip install flask
        ```
        ## 3.3 - pdf2image
        ```bash
            pip install pdf2image
        ```
        ## 3.4 -
        ```bash
            pip install poppler-utils
        ``` 
    ## 4 - Iniciar o flask
    ```bash
    python3 app.py
    ```

