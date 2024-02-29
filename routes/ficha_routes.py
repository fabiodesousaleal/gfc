from flask import Blueprint, jsonify, render_template, request, send_from_directory,send_file, abort

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
from data.data2 import *
from utils.cutter import gerar_codigo_cutter
from utils.utils import *

from models.ficha_model import FichaModel
from models.campus_model import CampusModel
from models.curso_model import CursoModel
from models.tipo_trabalho_model import TipoTrabalhoModel

ficha_routes = Blueprint('ficha_routes', __name__)

FONTE_SIZE = 10
CM_MEIO = 14.17 #meio centimetro
CM_UM = 28.35 #um centimetro
CM_UM_E_MEIO = 42.52 
CM_DOIS = 56.7
CM_TRES = 85.05 
CM_QUATRO = 4 * 28.35
CM_DOZE = 12 * 28.35

@ficha_routes.route("/")
def index():
    campus = CampusModel.get_campus()
    tipos_trabalho = TipoTrabalhoModel.get_tipos_trabalho()
    return render_template("form.html", campus=campus, tipos_trabalho=tipos_trabalho)

@ficha_routes.route("/get_cursos", methods=["POST"])
def get_cursos():
    dados = request.get_json()
    campus_id = dados.get('campus_id')
    cursos = CursoModel.get_cursos_by_campus_id(campus_id)
    cursos_serialized = CursoModel.serialize_cursos(cursos)
    return jsonify({'cursos': cursos_serialized})


@ficha_routes.route("/cutter", methods=["GET", "POST"])
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

def definir_tamanho_pagina(tipo_arquivo: str):
    if 'pdf' not in tipo_arquivo:
        return (12.25*28.35, 11*28.35)        
    return A4

def definir_y_retangulo(tipo_arquivo:str):
    if 'pdf' not in tipo_arquivo:
        return CM_DOIS
    return CM_QUATRO

def definir_estilo_paragrafos(fonte_nome)->dict:
    centralizado = ParagraphStyle(
        'paragrafo_centralizado',        
        alignment=1,  # 0=Left, 1=Center, 2=Right, 4=Justify        
        fontName = fonte_nome,
        fontSize = FONTE_SIZE,
    )

    justificado = ParagraphStyle(
        'paragrafo_justificado',
        alignment=4,  
        fontName=fonte_nome,
        fontSize=FONTE_SIZE,
        firstLineIndent=28.35        
    )

    a_esquerda = ParagraphStyle(
        'paragrafo_justificado',
        alignment=0,  
        fontName=fonte_nome,
        fontSize=FONTE_SIZE,               
    )

    justificado_sem_recuo = ParagraphStyle(
        'paragrafo_justificado',
        alignment=4,  # 0=Left, 1=Center, 2=Right, 4=Justify
        fontName=fonte_nome,
        fontSize=FONTE_SIZE,               
    )
    return {
        'centralizado': centralizado,
        'justificado': justificado,
        'a_esquerda': a_esquerda,
        'justificado_sem_recuo': justificado_sem_recuo
        }


@ficha_routes.route("/gerar_ficha", methods=["POST"])
def gerar_ficha():   
    dados=request.form.to_dict()
    
    campus = CampusModel.get_campus_by_id(dados["campus"])
    curso = CursoModel.get_curso_by_id(dados["curso"])
    tipo_trabalho = TipoTrabalhoModel.get_tipo_trabalho_by_id(dados["tipo-trabalho"])

    ficha=FichaModel(
        autor_nome=dados["autor-nome"],
        autor_sobrenome=dados["autor-sobrenome"],
        titulo_trabalho=dados["titulo-trabalho"],        
        folhas=dados["folhas"],
        campus=campus.nome,
        curso=curso,
        ano=dados["ano"],
        tipo_fonte=dados["tipo-fonte"],
        tipo_arquivo=dados["tipo-arquivo"],
        orientador_nome=dados['orientador-nome'],
        orientador_sobrenome=dados['orientador-sobrenome'],        
        assunto1=dados['assunto1'],
        assunto2=dados['assunto2'],
        assunto3=dados['assunto3'],
        assunto4=dados['assunto4'],
        coorientador_nome=dados['coorientador-nome'],
        coorientador_sobrenome=dados['coorientador-sobrenome'],
        tipo_trabalho=tipo_trabalho.nome,
        titulo_subtitulo=dados["titulo-subtitulo"],
    )

    tipo_arquivo=dados['tipo-arquivo']
    fonte_nome = ficha.tipo_fonte      

    registra_fontes()     
    
    tamanho_da_pagina = definir_tamanho_pagina(tipo_arquivo)

    c = canvas.Canvas('ficha.pdf', pagesize=tamanho_da_pagina)   
    c.setFont(fonte_nome, FONTE_SIZE)
   
    y_retangulo = definir_y_retangulo(tipo_arquivo)
    largura_pagina, altura_pagina = tamanho_da_pagina  
    x_retangulo = (largura_pagina - 12 * 28.35) / 2  
    largura_retangulo = 12 * 28.35  
    altura_retangulo = 7.5 * 28.35      

    # Desenha o retângulo
    c.rect(x_retangulo, y_retangulo, largura_retangulo, altura_retangulo)      
        
    paragrafos = ficha.get_paragrafos() 
    paragrafo_estilos = definir_estilo_paragrafos(fonte_nome)    
    
    #cabecalho1
    cabecalho1 = Paragraph(ficha.CABECALHO1, style=paragrafo_estilos['centralizado'])
    cabecalho1.wrap(largura_retangulo, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo  
    posicao_y_cabecalho1 = y_retangulo + altura_retangulo + 30  
    cabecalho1.drawOn(c, x_retangulo, posicao_y_cabecalho1 )  

    #cabecalho2
    cabecalho2 = Paragraph(ficha.CABECALHO2, style=paragrafo_estilos['centralizado'])
    cabecalho2.wrap(largura_retangulo, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo    
    posicao_y_cabecalho2 = posicao_y_cabecalho1 - cabecalho2.height
    cabecalho2.drawOn(c, x_retangulo, posicao_y_cabecalho2)

    #cabecalho3       
    paragrafo_estilos['centralizado'].fontName=fonte_nome+'-Bold' #alterando paragrafo centralizado para negrito
    cabecalho3 = Paragraph(ficha.CABECALHO3, style=paragrafo_estilos['centralizado'])
    cabecalho3.wrap(largura_retangulo + 10, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo    
    posicao_y_cabecalho3 = posicao_y_cabecalho2 - cabecalho3.height
    cabecalho3.drawOn(c, x_retangulo -7, posicao_y_cabecalho3)  

    #CODIGO CUTTER
    codigo_cutter = ficha.get_codigo_cutter()
    c.drawString(x_retangulo + CM_MEIO/2, y_retangulo + altura_retangulo - CM_UM, codigo_cutter)

    #DEFINE A POSIÇÃO do eixo X para ser aplicado nos paragrafos
    posicao_x_paragrafos = x_retangulo + CM_UM_E_MEIO

    #PARAGRAFO 1  -  Fabio, Leal 
    
    p1 = Paragraph(paragrafos[1], style=paragrafo_estilos['a_esquerda'])
    p1.wrap(largura_retangulo - 2 * 28.35, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo
    posicao_y_p1 = y_retangulo + altura_retangulo - p1.height - 20 # define o eixo y que sera apresentado o paragrafo1.
    p1.drawOn(c, posicao_x_paragrafos , posicao_y_p1)       

    #PARAGRAFO 2 - Protocolo de Roteamento IPV6: A Eficiencia do IPv6. / Fábio de Sousa Leal, Araguaína, 2024 ...etc  
    p2 = Paragraph(paragrafos[2], style=paragrafo_estilos['justificado'])
    p2.wrap(largura_retangulo - 2 * 28.35, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo
    posicao_y_p2 = posicao_y_p1 - p2.height
    p2.drawOn(c, posicao_x_paragrafos, posicao_y_p2) 

    #PARAGRAFO 3 - 26 f. 
    p3 = Paragraph(paragrafos[3], style=paragrafo_estilos['justificado'])
    p3.wrap(largura_retangulo - 2 * 28.35, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo
    posicao_y_p3 = posicao_y_p2 - p3.height
    p3.drawOn(c, posicao_x_paragrafos, posicao_y_p3)  

    #PARAGRAFO 4 - Monografia Graduação - Universidade Federal do Tocantins – ... etc
    p4 = Paragraph(paragrafos[4], style=paragrafo_estilos['justificado'])
    p4.wrap(largura_retangulo - 2 * 28.35, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo
    posicao_y_p4 = posicao_y_p3 - p4.height - CM_MEIO/2
    p4.drawOn(c, posicao_x_paragrafos, posicao_y_p4 )

    #PARAGRAFO 5 - Orientador 
    p5 = Paragraph(paragrafos[5], style=paragrafo_estilos['justificado'])
    p5.wrap(largura_retangulo - 2 * 28.35, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo
    posicao_y_p5 = posicao_y_p4 - p5.height - CM_MEIO/2
    p5.drawOn(c, posicao_x_paragrafos, posicao_y_p5)

    if ficha.coorientador_nome:
        #PARAGRAFO 6 - Coorientador 
        p6 = Paragraph(paragrafos[6], style=paragrafo_estilos['justificado'])
        p6.wrap(largura_retangulo - 2 * 28.35, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo
        posicao_y_p6 = posicao_y_p5 - p6.height
        p6.drawOn(c, posicao_x_paragrafos, posicao_y_p6)    

        #PARAGRAFO 7 - ASSUNTOS 
        p7 = Paragraph(paragrafos[7], style=paragrafo_estilos['justificado'])
        p7.wrap(largura_retangulo - 2 * 28.35, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo
        posicao_y_p7 = posicao_y_p6 - p7.height - CM_MEIO/2
        p7.drawOn(c, posicao_x_paragrafos, posicao_y_p7)

    else:
        #PARAGRAFO 7 - ASSUNTOS 
        p7 = Paragraph(paragrafos[7], style=paragrafo_estilos['justificado'])
        p7.wrap(largura_retangulo - 2 * 28.35, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo
        posicao_y_p7 = posicao_y_p5 - p7.height - CM_MEIO/2
        p7.drawOn(c, posicao_x_paragrafos, posicao_y_p7)

    

    # CDD
    c.setFont(fonte_nome+"-Bold", FONTE_SIZE)
    c.drawString(x_retangulo + 10*28.35 - CM_MEIO/2, y_retangulo + CM_MEIO, ficha.get_cdd())

    #RODAPE 5      
    r = Paragraph(ficha.RODAPE, style=paragrafo_estilos['justificado_sem_recuo'])
    r.wrap(largura_retangulo, altura_retangulo) # aqui vai ficar um recuo 0,5 cm da borda direita do retangulo    
    r.drawOn(c, x_retangulo, y_retangulo - r.height)

    # Salvando o PDF
    c.save()

    if 'img' not in tipo_arquivo:
        return send_from_directory("", "ficha.pdf", as_attachment=True)
        
    images = convert_from_path('ficha.pdf') 
    img_io = io.BytesIO()
    images[0].save(img_io, 'PNG')
    os.remove('ficha.pdf')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')      
       

   
