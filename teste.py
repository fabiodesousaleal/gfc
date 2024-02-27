from models.campus_model import CampusModel

#curso = CursoModel.get_curso_by_id(110)
#print(curso)

#for campus in cursos:
#    print(f"ID: {campus.id}, Nome: {campus.nome}")
#curso.remove()
#novo_campus = CampusModel("Imperatriz",1)
#novo_campus.save()
teste = CampusModel.get_campus_by_id(7)
teste.nome='ARAGUAIA'

teste.save()

campus = CampusModel.get_campus()
for campus in campus:
    print(f"ID: {campus.id}, Nome: {campus.nome}")