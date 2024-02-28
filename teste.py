from models.curso_model import CursoModel
cursos=CursoModel.get_cursos()
for curso in cursos:
    print(curso.get_campus()) 