# campus_model.py
import sqlite3
from data.conexao import get_conexao

class CampusModel:
    def __init__(self, nome, ativo=1, id=None):
        self.id = id
        self.nome = nome
        self.ativo = ativo

    @classmethod
    def get_campus(cls):
        con = get_conexao()
        cursor = con.cursor()
        query = 'SELECT * FROM campus'
        cursor.execute(query)
        campus_list = []

        for row in cursor.fetchall():
            campus = cls(
                id=row[0],
                nome=row[1],
                ativo=row[2]
            )
            campus_list.append(campus)

        con.close()
        return campus_list

    def save(self):
        con = get_conexao()
        cursor = con.cursor()

        if self.id is None:
            # Se o id não estiver definido, é uma nova inserção
            query = 'INSERT INTO campus (nome, ativo) VALUES (?, ?)'
            cursor.execute(query, (self.nome, self.ativo))
        else:
            # Se o id estiver definido, é uma atualização
            query = 'UPDATE campus SET nome=?, ativo=? WHERE id=?'
            cursor.execute(query, (self.nome, self.ativo, self.id))

        con.commit()
        con.close()

    def remove(self):
        con = get_conexao()
        cursor = con.cursor()

        if self.id is not None:
            # Se o id estiver definido, remove o campus com base no id
            query = 'DELETE FROM campus WHERE id=?'
            cursor.execute(query, (self.id,))

        con.commit()
        con.close()

    @staticmethod
    def get_campus_by_id(campus_id):
        con = get_conexao()
        cursor = con.cursor()
        query = 'SELECT * FROM campus WHERE id=?'
        cursor.execute(query, (campus_id,))
        row = cursor.fetchone()

        if row:
            campus = CampusModel(
                id=row[0],
                nome=row[1],
                ativo=row[2]
            )
            con.close()
            return campus
        else:
            con.close()
            return None   
           
       
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'ativo': self.ativo           
        }
    
    @staticmethod
    def serialize(itens):
        serialized_list = []
        for item in itens:
            serialized_list.append(item.to_dict())
        return serialized_list

    def __str__(self) -> str:
        return self.nome