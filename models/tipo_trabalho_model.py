# tipo_trabalho_model.py
import sqlite3
from data.conexao import get_conexao

class TipoTrabalhoModel:
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

    def save(self):
        con = get_conexao()
        cursor = con.cursor()

        if self.id is None:
            query = 'INSERT INTO tipo_trabalho (nome, ativo) VALUES (?, ?)'
            cursor.execute(query, (self.nome, self.ativo))
        else:
            query = 'UPDATE tipo_trabalho SET nome=?, ativo=? WHERE id=?'
            cursor.execute(query, (self.nome, self.ativo, self.id))

        con.commit()
        con.close()

    def remove(self):
        con = get_conexao()
        cursor = con.cursor()

        if self.id is not None:
            query = 'DELETE FROM tipo_trabalho WHERE id=?'
            cursor.execute(query, (self.id,))

        con.commit()
        con.close()

    @staticmethod
    def get_tipo_trabalho_by_id(tipo_trabalho_id):
        con = get_conexao()
        cursor = con.cursor()
        query = 'SELECT * FROM tipo_trabalho WHERE id=?'
        cursor.execute(query, (tipo_trabalho_id,))
        row = cursor.fetchone()

        if row:
            tipo_trabalho = TipoTrabalhoModel(
                id=row[0],
                nome=row[1],
                ativo=row[2]
            )
            con.close()
            return tipo_trabalho
        else:
            con.close()
            return None
    
    def __str__(self) -> str:
        return self.nome
