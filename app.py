from flask import Flask, render_template, request, send_from_directory,send_file, abort
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib import colors
from pdf2image import convert_from_path
import os
import io
from data.data import *
from utils.cutter import gerar_codigo_cutter
from utils.utils import *
from models.ficha_model import FichaModel


app = Flask(__name__)

FONTE_SIZE = 10
CM_MEIO = 14.17 #meio centimetro
CM_UM = 28.35 #um centimetro
CM_UM_E_MEIO = 42.52 
CM_DOIS = 56.7
CM_TRES = 85.05 
CM_QUATRO = 4 * 28.35
CM_DOZE = 12 * 28.35

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/cutter", methods=["GET", "POST"])
def cutter():
    if request.method == 'GET':
        return render_template("form_cutter.html")
    elif request.method == 'POST':
        dados = request.form.to_dict()         
        sobrenome = dados['sobrenome'] 
        titulo = dados['titulo']
        codigo_cutter = gerar_codigo_cutter(sobrenome, titulo)
        return render_template("form_cutter.html", codigo_cutter=codigo_cutter, sobrenome=sobrenome)       
    else:
        abort(405)


@app.route("/gerar_ficha", methods=["POST"])
def gerar_ficha():   
    dados = request.form.to_dict()
    ficha = FichaModel(
        autor_nome = dados["autor-nome"],
        autor_sobrenome = dados["autor-sobrenome"],
        titulo_trabalho= dados["titulo-trabalho"],
        titulo_subtitulo = dados["titulo-subtitulo"],
        folhas = dados["folhas"],
        campus = dados["campus"],
        curso = dados["curso"],
        ano = dados["ano"],
        tipo_fonte = dados["tipo-fonte"],
        tipo_arquivo = dados["tipo-arquivo"],
    )       
    tipo_arquivo = dados['tipo-arquivo']
    fonte_nome = ficha.tipo_fonte
      

    registra_fontes()     
    #Define o tamanho da pagina e outras variaveis com base no tipo de arquivo        
    if tipo_arquivo == 'img':
        tamanho_da_pagina = (12.25*28.35, 11*28.35)
        y_retangulo = CM_DOIS
    else:
        tamanho_da_pagina = A4
        y_retangulo = CM_QUATRO

    c = canvas.Canvas('ficha.pdf', pagesize=tamanho_da_pagina)   
    # Definindo a fonte e o tamanho do texto

    c.setFont(fonte_nome, FONTE_SIZE) 

    # Coordenadas e dimensões do retângulo 
    largura_pagina, altura_pagina = tamanho_da_pagina  # largura_pagina = 595.276 e altura_pagina = 841.889
    x_retangulo = (largura_pagina - 12 * 28.35) / 2 #linha com 12cm  
    largura_retangulo = 12 * 28.35  # Convertendo de cm para pontos
    altura_retangulo = 7.5 * 28.35  # Convertendo de cm para pontos     

    # Desenha o retângulo
    c.rect(x_retangulo, y_retangulo, largura_retangulo, altura_retangulo)     
        
    estilo_paragrafo_centralizado = ParagraphStyle(
        'paragrafo_centralizado',        
        alignment=1,  # 0=Left, 1=Center, 2=Right        
        fontName = fonte_nome,
        fontSize = FONTE_SIZE,
    )

    estilo_paragrafo_justificado = ParagraphStyle(
        'paragrafo_justificado',
        alignment=4,  # 0=Left, 1=Center, 2=Right, 4=Justify
        fontName=fonte_nome,
        fontSize=FONTE_SIZE,
        firstLineIndent=28.35        
    )

    estilo_paragrafo_alinhado_a_esquerda = ParagraphStyle(
        'paragrafo_justificado',
        alignment=0,  # 0=Left, 1=Center, 2=Right, 4=Justify
        fontName=fonte_nome,
        fontSize=FONTE_SIZE,               
    )

    estilo_paragrafo_justificado_sem_recuo = ParagraphStyle(
        'paragrafo_justificado',
        alignment=4,  # 0=Left, 1=Center, 2=Right, 4=Justify
        fontName=fonte_nome,
        fontSize=FONTE_SIZE,               
    )
    paragrafos = ficha.get_paragrafos(dados)    
    #C1
    c1 = Paragraph(ficha.CABECALHO1, style=estilo_paragrafo_centralizado)
    c1.wrap(largura_retangulo, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo  
    posicao_y_c1 = y_retangulo + altura_retangulo + 30  
    c1.drawOn(c, x_retangulo, posicao_y_c1 )  

    #C2
    c2 = Paragraph(ficha.CABECALHO2, style=estilo_paragrafo_centralizado)
    c2.wrap(largura_retangulo, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo    
    posicao_y_c2 = posicao_y_c1 - c2.height
    c2.drawOn(c, x_retangulo, posicao_y_c2)

    #C3       
    estilo_paragrafo_centralizado.fontName=fonte_nome+'-Bold' #alterando paragrafo centralizado para negrito
    c3 = Paragraph(ficha.CABECALHO3, style=estilo_paragrafo_centralizado)
    c3.wrap(largura_retangulo + 10, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo    
    posicao_y_c3 = posicao_y_c2 - c3.height
    c3.drawOn(c, x_retangulo -7, posicao_y_c3)  

    #CODIGO CUTTER
    codigo_cutter = ficha.get_codigo_cutter()
    c.drawString(x_retangulo + CM_MEIO, y_retangulo + altura_retangulo - CM_UM, codigo_cutter)

    #DEFINE A POSIÇÃO do eixo X para ser aplicado nos paragrafos
    posicao_x_paragrafos = x_retangulo + CM_UM_E_MEIO

    #PARAGRAFO 1  -  nome cientifico  
    
    p1 = Paragraph(paragrafos[1], style=estilo_paragrafo_alinhado_a_esquerda)
    p1.wrap(largura_retangulo - 2 * 28.35, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo
    posicao_y_p1 = y_retangulo + altura_retangulo - p1.height - 20 # define o eixo y que sera apresentado o paragrafo1.
    p1.drawOn(c, posicao_x_paragrafos , posicao_y_p1)       

    #PARAGRAFO 2 - titulo, subtitulo, nome completo, cidade, ano  
    p2 = Paragraph(paragrafos[2], style=estilo_paragrafo_justificado)
    p2.wrap(largura_retangulo - 2 * 28.35, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo
    posicao_y_p2 = posicao_y_p1 - p2.height
    p2.drawOn(c, posicao_x_paragrafos, posicao_y_p2) 

    #PARAGRAFO 3 - quantidade de folhas 
    p3 = Paragraph(paragrafos[3], style=estilo_paragrafo_justificado)
    p3.wrap(largura_retangulo - 2 * 28.35, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo
    posicao_y_p3 = posicao_y_p2 - p3.height
    p3.drawOn(c, posicao_x_paragrafos, posicao_y_p3)  

    #PARAGRAFO 4 - tipo graduacao, nome do curso  
    p4 = Paragraph(paragrafos[4], style=estilo_paragrafo_justificado)
    p4.wrap(largura_retangulo - 2 * 28.35, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo
    posicao_y_p4 = posicao_y_p3 - p4.height
    p4.drawOn(c, posicao_x_paragrafos, posicao_y_p4)

    #PARAGRAFO 5 - assuntos 
    p5 = Paragraph(paragrafos[5], style=estilo_paragrafo_justificado)
    p5.wrap(largura_retangulo - 2 * 28.35, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo
    posicao_y_p5 = posicao_y_p4 - p5.height
    p5.drawOn(c, posicao_x_paragrafos, posicao_y_p5)

    # CDD
    c.setFont(fonte_nome+"-Bold", FONTE_SIZE)
    c.drawString(x_retangulo + 10*28.35, y_retangulo + CM_MEIO, ficha.get_cdd())

    #RODAPE 5      
    r = Paragraph(ficha.RODAPE, style=estilo_paragrafo_justificado_sem_recuo)
    r.wrap(largura_retangulo, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo    
    r.drawOn(c, x_retangulo, y_retangulo - r.height)

    # Salvando o PDF
    c.save()

    if tipo_arquivo == 'pdf':
        return send_from_directory("", "ficha.pdf", as_attachment=True)

    if tipo_arquivo == 'img':
        # Converta o PDF em uma imagem
        images = convert_from_path('ficha.pdf')
        
        width, height = images[0].size
        print(f'dimensoes do pdf wid: {width} e o height:{height}')

        # Redimensione a imagem para as mesmas dimensões do PDF
        #images[0] = images[0].resize((482, 433))

        # Salve a primeira página do PDF como uma imagem na memória
        img_io = io.BytesIO()

        images[0].save(img_io, 'PNG')

        # Apague o arquivo PDF
        os.remove('ficha.pdf')

        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')      
       
if __name__ == "__main__":
    app.run(debug=True)
