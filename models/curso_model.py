import sqlite3
from data.conexao import get_conexao
from .campus_model import CampusModel

class CursoModel:
    def __init__(self, nome, cdd, campus_id, tipo, ativo, id=None ) -> None:
        self.id=id
        self.nome=nome
        self.cdd=cdd
        self.campus=campus_id
        self.tipo=tipo
        self.ativo=ativo
    
    @staticmethod
    def get_cursos():
        con = get_conexao()
        cursor = con.cursor()
        query = 'SELECT * FROM curso'
        cursor.execute(query)
        cursos = []

        for row in cursor.fetchall():
            curso = CursoModel(
                id=row[0],
                nome=row[1],
                cdd=row[2],
                campus_id=row[3],
                tipo=row[4],
                ativo=row[5]
            )
            cursos.append(curso)
        con.close()        
        
        if not cursos:
            return None
        return cursos 

    
    @staticmethod
    def get_curso_by_id(curso_id):
        con = get_conexao()
        cursor = con.cursor()
        query = 'SELECT * FROM curso WHERE id=?'
        cursor.execute(query, (curso_id,))
        row = cursor.fetchone()

        if row:
            curso = CursoModel(
                id=row[0],
                nome=row[1],
                cdd=row[2],
                campus_id=row[3],
                tipo=row[4],
                ativo=row[5]
            )
            con.close()
            return curso
        else:
            con.close()
            return None
    
    
    def remove(self):
        con = get_conexao()
        cursor = con.cursor()
        if self.id is not None:
            query = 'DELETE FROM curso WHERE id=?'
            cursor.execute(query, (self.id,))
        con.commit()
        con.close()

    def get_campus(self):
        if self.campus_id is not None:            
            return CampusModel.get_campus_by_id(self.campus_id)
        else:
            return None
    
    def __str__(self) -> str:
        return self.nome
        




