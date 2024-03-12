from utils.cutter import gerar_codigo_cutter

from models.curso_model import CursoModel
from models.campus_model import CampusModel
from models.tipo_trabalho_model import TipoTrabalhoModel
from models.parametro_model import ParametroModel
from data.data2 import *

class FichaModel:
    def __init__(self,
                 parametro: ParametroModel, 
                 autor_nome,
                 autor_sobrenome,
                 titulo_trabalho,                 
                 folhas,
                 campus: CampusModel,
                 curso: CursoModel,
                 ano,
                 tipo_fonte,
                 tipo_arquivo,
                 orientador_nome,
                 orientador_sobrenome,
                 orientador_feminino,                 
                 assunto1,
                 assunto2,
                 assunto3,
                 tipo_trabalho: TipoTrabalhoModel,
                 coorientador_nome=None,
                 coorientador_sobrenome=None,
                 coorientador_feminino = None,
                 titulo_subtitulo=None,
                 autor2_nome=None,
                 autor2_sobrenome=None,
                 autor3_nome=None,
                 autor3_sobrenome=None,
                   ) -> None:
        self.parametro = parametro
        self.autor_nome = autor_nome
        self.autor_sobrenome = autor_sobrenome
        self.titulo_trabalho = titulo_trabalho
        self.titulo_subtitulo = titulo_subtitulo
        self.folhas = folhas
        self.campus = campus
        self.curso = curso
        self.ano = ano
        self.tipo_fonte = tipo_fonte
        self.tipo_arquivo = tipo_arquivo
        self.orientador_nome = orientador_nome
        self.orientador_sobrenome = orientador_sobrenome
        self.orientador_feminino = orientador_feminino
        self.coorientador_nome = coorientador_nome
        self.coorientador_sobrenome = coorientador_sobrenome
        self.coorientador_feminino = coorientador_feminino
        self.assunto1 = assunto1
        self.assunto2 = assunto2
        self.assunto3 = assunto3
        self.tipo_trabalho = tipo_trabalho
        self.autor2_nome=autor2_nome
        self.autor2_sobrenome=autor2_sobrenome
        self.autor3_nome=autor3_nome
        self.autor3_sobrenome=autor3_sobrenome

            

    def get_codigo_cutter(self)-> str:   
        return gerar_codigo_cutter(self.autor_sobrenome, self.titulo_trabalho)
        
    #def get_codigo_cdd(self, autor_curso):
    def get_paragrafos(self):

        autor_nome_completo = f'{self.autor_nome} {self.autor_sobrenome}' 
        orientador = f'{self.orientador_sobrenome}, {self.orientador_nome}'
        coorientador = f'{self.coorientador_sobrenome}, {self.coorientador_nome}'
        orientadores = f'I. {orientador}, orient. II. {coorientador},  Título.'

        autores = autor_nome_completo

        #CONTRUINDO O PARAGRAFO 1
        paragrafo1 = f'{self.autor_sobrenome}, {self.autor_nome}.'

        
             
       #ASSUNTOS E AUTORES
        assuntos = f'1. {self.assunto1}. 2. {self.assunto2}. 3. {self.assunto3}.'

        if self.autor2_nome:
            assuntos = f'{assuntos} I. {self.autor2_sobrenome}, {self.autor2_nome}.' 
            autores = f'{autores}, {self.autor2_nome} {self.autor2_sobrenome}'   
        if self.autor2_nome and not self.autor3_nome:
            assuntos = f'{assuntos} II. Título'

        if self.autor2_nome and self.autor3_nome:
            assuntos = f'{assuntos} II. {self.autor3_sobrenome}, {self.autor3_nome}. III. Título.' 
            autores = f'{autores}, {self.autor3_nome} {self.autor3_sobrenome}'     
        
        # CONSTRUINDO PARAGRAFO 2                        
        paragrafo2 = f'{self.titulo_trabalho}: {self.titulo_subtitulo} / {autores}. - {self.campus}, TO, {self.ano}.'
        
        if not self.titulo_subtitulo:
            paragrafo2 = f'{self.titulo_trabalho} / {autor_nome_completo}. - {self.campus}, TO, {self.ano}.'       

        #CONSTRUINDO PARAGRAFO 3 e 4
        paragrafo3 = f'{self.folhas} f.'
        paragrafo4 = f'{self.tipo_trabalho} ({self.curso.tipo} - {self.curso.nome}) -- {self.parametro.instituicao}, {self.ano}.'
        
        #CONSTRUINDO PARAGRAFO 5  e 6   
        paragrafo5 = f'Orientador: {self.orientador_nome} {self.orientador_sobrenome}.'

        if self.orientador_feminino:
            paragrafo5 = f'Orientadora: {self.orientador_nome} {self.orientador_sobrenome}.'
        
        paragrafo6 = f'Coorientador: {self.coorientador_nome} {self.coorientador_sobrenome}.'
        
        if self.coorientador_feminino:
            paragrafo6 = f'Coorientadora: {self.coorientador_nome} {self.coorientador_sobrenome}.'
        
        
        #CONSTRUINDO PARAGRAFO 7
        
        paragrafo7 = f'{assuntos}'       
        paragrafos = {
            1: paragrafo1,
            2: paragrafo2,
            3: paragrafo3,
            4: paragrafo4,
            5: paragrafo5,
            6: paragrafo6,
            7: paragrafo7 
            }
        return paragrafos
  
    
    def get_cdd(self)->str:
        return f'CDD {self.curso.cdd}'