from models.curso_model import CursoModel
cursos=CursoModel.get_cursos_by_campus_id(campus_id=2)
all = CursoModel.serialize_cursos(cursos)
print(all)