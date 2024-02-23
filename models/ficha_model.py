from utils.cutter import gerar_codigo_cutter
from data.data import *

class FichaModel:
    CABECALHO1 = "Dados Internacionais de Catalogação na Publicação (CIP)"
    CABECALHO2 = "Sistema de Geração de Ficha Catalografica SGFC-UFNT" 
    CABECALHO3 = "Gerado automaticamente mediante os dados fornecidos pelo(a) autor(a)"
    INSTITUICAO ='Universidade Federal do Norte do Tocantins'   
    RODAPE = "TODOS OS DIREITOS RESERVADOS – A reprodução total ou parcial, de qualquer forma ou por qualquer meio deste documento é autorizado desde que citada a fonte. A violação dos direitos do autor (Lei nº 9.610/98) é crime estabelecido pelo artigo 184 do Código Penal."

    def __init__(self, autor_nome, autor_sobrenome, titulo_trabalho, titulo_subtitulo, folhas, campus, curso, ano, tipo_fonte, tipo_arquivo ) -> None:
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

    def get_codigo_cutter(self)-> str:   
        return gerar_codigo_cutter(self.autor_sobrenome, self.titulo_trabalho)
        
    #def get_codigo_cdd(self, autor_curso):
    def get_paragrafos(self, dados):            
        assunto1 = dados['assunto1']
        assunto2 = dados['assunto2']
        assunto3 = dados['assunto3']
        assunto4 = dados['assunto4']
        assunto5 = dados['assunto5'] 
        assuntos = f'1. {assunto1}. 2. {assunto2}. 3. {assunto3}. 4. {assunto4}. 5. {assunto5}. '     
        orientador = f'{dados["orientador-sobrenome"]}, {dados["orientador-nome"]}'
        coorientador = f'{dados["coorientador-sobrenome"]}, {dados["coorientador-nome"]}'
        orientadores = f'I. {orientador}, orient. II. {coorientador},  Título.'
        paragrafo5 = assuntos+orientadores
        autor_nome_completo = f'{dados["autor-nome"]} {dados["autor-sobrenome"]}'    
        paragrafo1 = f'{dados["autor-sobrenome"]}, {dados["autor-nome"]}.'
        paragrafo2 = f'{dados["titulo-trabalho"]}: {dados["titulo-subtitulo"]}. / {autor_nome_completo}. - {dados["campus"]}, TO, {dados["ano"]}.' 
        paragrafo3 = f'{dados["folhas"]} f.'
        paragrafo4 = f'{tipo_trabalho[dados["tipo-trabalho"]]} ({tipo_ensino["1"]} - {cursos[dados["curso"]]}) --{self.INSTITUICAO}, {dados["ano"]}'
        
        paragrafos = {
            1: paragrafo1,
            2: paragrafo2,
            3: paragrafo3,
            4: paragrafo4,
            5: paragrafo5, 
            }
        return paragrafos
  
    
    def get_cdd(self)->str:
        return '510'