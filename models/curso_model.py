import sqlite3
from data.conexao import get_conexao
from .campus_model import CampusModel
from .base_model import ClasseBase

class CursoModel(ClasseBase):

    tabela = 'curso'
    
    def __init__(self, nome, cdd, campus_id, tipo, ativo, id=None ) -> None:
        self.id=id
        self.nome=nome
        self.cdd=cdd
        self.campus_id=campus_id
        self.tipo=tipo
        self.ativo=ativo
 
    @staticmethod
    def get_cursos_by_campus_id(campus_id):
        con = get_conexao()
        cursor = con.cursor()
        query = 'SELECT * FROM curso WHERE campus_id=?'
        cursor.execute(query, (campus_id,))
        cursos_list = []

        for row in cursor.fetchall():
            campus = CursoModel(
                id=row[0],
                nome=row[1],
                cdd=row[2],
                campus_id=row[3],
                tipo=row[4],
                ativo=row[5]
            )
            cursos_list.append(campus)

        con.close()
        return cursos_list    
   
        
     
    def get_campus(self):
        if self.campus_id is not None:            
            return CampusModel.get_by_id(self.campus_id)
        else:
            return None
        
         
    def __str__(self) -> str:
        return self.nome
        




