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
                 assunto4,
                 tipo_trabalho: TipoTrabalhoModel,
                 coorientador_nome=None,
                 coorientador_sobrenome=None,
                 coorientador_feminino = None,
                 titulo_subtitulo=None,
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
        self.orintador_feminino = orientador_feminino
        self.coorientador_nome = coorientador_nome
        self.coorientador_sobrenome = coorientador_sobrenome
        self.coorientador_feminino = coorientador_feminino
        self.assunto1 = assunto1
        self.assunto2 = assunto2
        self.assunto3 = assunto3
        self.assunto4 = assunto4
        self.tipo_trabalho = tipo_trabalho

            

    def get_codigo_cutter(self)-> str:   
        return gerar_codigo_cutter(self.autor_sobrenome, self.titulo_trabalho)
        
    #def get_codigo_cdd(self, autor_curso):
    def get_paragrafos(self): 
             
        assuntos = f'1. {self.assunto1}. 2. {self.assunto2}. 3. {self.assunto3}. 4. {self.assunto4}. '     
        orientador = f'{self.orientador_sobrenome}, {self.orientador_nome}'
        coorientador = f'{self.coorientador_sobrenome}, {self.coorientador_nome}'
        orientadores = f'I. {orientador}, orient. II. {coorientador},  Título.'
        paragrafo5 = assuntos+orientadores
        autor_nome_completo = f'{self.autor_nome} {self.autor_sobrenome}'    
        paragrafo1 = f'{self.autor_sobrenome}, {self.autor_nome}.'
        paragrafo2 = f'{self.titulo_trabalho}: {self.titulo_subtitulo}. / {autor_nome_completo}. - {self.campus}, TO, {self.ano}.' 
        
        if not self.titulo_subtitulo:
            paragrafo2 = f'{self.titulo_trabalho}. / {autor_nome_completo}. - {self.campus}, TO, {self.ano}.' 

        paragrafo3 = f'{self.folhas} f.'
        paragrafo4 = f'{self.tipo_trabalho} ({self.curso.tipo} - {self.curso.nome}) --{self.parametro.instituicao}, {self.ano}.' 
        
        paragrafo5 = f'Orientador: {self.orientador_nome} {self.orientador_sobrenome}.'

        if self.orintador_feminino:
            paragrafo5 = f'Orientadora: {self.orientador_nome} {self.orientador_sobrenome}.'
        
        paragrafo6 = f'Coorientador: {self.coorientador_nome} {self.coorientador_sobrenome}.'
        
        if self.coorientador_feminino:
            paragrafo6 = f'Coorientadora: {self.coorientador_nome} {self.coorientador_sobrenome}.'
        
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