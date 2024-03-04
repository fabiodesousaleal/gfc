# tipo_trabalho_model.py
import sqlite3
from data.conexao import get_conexao
from models.base_model import ClasseBase

class TipoTrabalhoModel(ClasseBase):

    tabela = "tipo_trabalho"
    
    def __init__(self, nome, ativo=1, id=None):
        self.id = id
        self.nome = nome
        self.ativo = ativo

    @classmethod
    def get_tipos_trabalho(cls):
        con = get_conexao()
        cursor = con.cursor()
        query = 'SELECT * FROM tipo_trabalho'
        cursor.execute(query)
        tipos_trabalho_list = []

        for row in cursor.fetchall():
            tipo_trabalho = cls(
                id=row[0],
                nome=row[1],
                ativo=row[2]
            )
            tipos_trabalho_list.append(tipo_trabalho)

        con.close()
        return tipos_trabalho_list
  

    def remove(self):
        con = get_conexao()
        cursor = con.cursor()

        if self.id is not None:
            query = 'DELETE FROM tipo_trabalho WHERE id=?'
            cursor.execute(query, (self.id,))

        con.commit()
        con.close()   
    
    
    def __str__(self) -> str:
        return self.nome
