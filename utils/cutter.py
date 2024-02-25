#Desenvolvido por: Fábio Leal
#falta refatorar
from utils.data_cutter import get_data_cutter
import unicodedata

def remover_acentos(string):
    normalized_string = unicodedata.normalize('NFD', string)    
    return (''.join(char for char in normalized_string if unicodedata.category(char) != 'Mn' or char == "'")).replace("'", "")

def primeira_letra_sem_artigos(titulo):
    artigos = ['O', 'A', 'Os', 'As', 'Um', 'Uma', 'Uns']
    palavras = titulo.split()  
    palavras_sem_artigos = [palavra for palavra in palavras if palavra not in artigos]
    primeira_letra = palavras_sem_artigos[0][0] if palavras_sem_artigos else ''
    return primeira_letra

def get_item_com_menor_quantidade_caracteres_no_valor(items, lista_codigo_fator):    
    if not items:
        return None
    menor_codigo = None
    menor_quantidade = float('inf')     
    for cod, nome in items:
        if cod in lista_codigo_fator:
            quantidade_caracteres = len(nome)     
            if quantidade_caracteres < menor_quantidade:
                menor_codigo = cod
                menor_quantidade = quantidade_caracteres                           
    return menor_codigo

def gerar_codigo_cutter(autor_sobrenome: str, titulo: str )-> str:
    autor_sobrenome = autor_sobrenome.lower()
    autor_sobrenome = remover_acentos(autor_sobrenome)
    dados = get_data_cutter()
    for letra, itens in dados.items():          
        if letra == autor_sobrenome[0]:
            lista_codigo_fator = get_lista_codigo_fator(autor_sobrenome, itens)
            lista_fatores = [valor for chave, valor in lista_codigo_fator]
            maior_fator = max(lista_fatores, default=None)
            lista_de_codigo_fator = [(chave) for chave, valor in lista_codigo_fator if valor == maior_fator]
            if len(lista_de_codigo_fator) > 1:
                codigo=get_item_com_menor_quantidade_caracteres_no_valor(itens, lista_de_codigo_fator)               
            else:                
                codigo=lista_de_codigo_fator[0]                 
        
    return autor_sobrenome[0].upper()+str(codigo)+primeira_letra_sem_artigos(titulo).lower()        


def gerar_fator_semelhanca(sobrenome_procurado, sobrenome_tabela):
    i = 0
    somatorio = 0
    sobrenome_is_menor = False
    if len(sobrenome_procurado) > len(sobrenome_tabela):
        sobrenome_is_menor = False
        sobrenome_procurado = sobrenome_procurado[:len(sobrenome_tabela)]                   
    elif len(sobrenome_procurado) < len(sobrenome_tabela):        
        sobrenome_is_menor = True

    while i <= len(sobrenome_procurado)-1:          
        if sobrenome_procurado[i] == sobrenome_tabela[i]:            
            somatorio += ord(sobrenome_tabela[i])
            
            if sobrenome_is_menor and len(sobrenome_procurado)-1 == i :
                somatorio -= ord(sobrenome_tabela[i]) 

        else:
            if sobrenome_tabela[i] < sobrenome_procurado[i]:              
                somatorio += ord(sobrenome_tabela[i])
                break
            else:
                break
        i+=1    
    return somatorio

def get_lista_codigo_fator(autor_sobrenome, cutter_data):
    lista_codigo_fator = []        
    for item in cutter_data:
        codigo, valor = item
        fator_semelhanca = gerar_fator_semelhanca(autor_sobrenome, valor)
        novo_item = (codigo, fator_semelhanca)
        lista_codigo_fator.append(novo_item)  
    return lista_codigo_fator         

