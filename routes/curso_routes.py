from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from flask_login import login_required
from models.curso_model import CursoModel
from models.campus_model import CampusModel


curso_routes = Blueprint('curso_routes',__name__)


@curso_routes.route('/', methods=['GET', 'POST'])
@login_required
def curso_listar():
    cursos = CursoModel.get_cursos()
    campus = CampusModel.get_campus()
    return render_template('cursos_view.html', cursos=cursos, campus=campus)


@curso_routes.route('/save', methods=['POST'])
def save_curso():
    success_message = None
    error_message = None

    if request.method == 'POST':
        dados = request.form.to_dict()
        id = dados.get('curso_id')

        try:
            if id:
                curso = CursoModel.get_curso_by_id(id)
                if curso:
                    curso.nome = dados.get('nome')
                    curso.cdd = dados.get('cdd')
                    curso.campus_id = dados.get('campus_id')
                    curso.tipo = dados.get('tipo')
                    curso.ativo = dados.get('ativo')
                    success_message = 'Curso atualizado com sucesso!'
                else:
                    error_message = 'Curso não encontrado'
            else:
                curso = CursoModel(
                    nome=dados.get('nome'),
                    cdd=dados.get('cdd'),
                    campus_id=dados.get('campus_id'),
                    tipo=dados.get('tipo'),
                    ativo=dados.get('ativo')
                )

                success_message = 'Curso criado com sucesso!'

            curso.save()
        except Exception as e:
            error_message = f'Erro ao salvar curso: {str(e)}'

    cursos = CursoModel.get_cursos()
    campus = CampusModel.get_campus()

    return render_template('cursos_view.html', campus=campus, cursos=cursos, success_message=success_message, error_message=error_message )


@curso_routes.route('/editar', methods=["POST"])
@login_required
def teste():
    dados = request.get_json()
    curso_id = dados.get("curso_id")
    curso = CursoModel.get_curso_by_id(curso_id)
    if curso:
        return jsonify(curso.to_dict())
    else:
        return jsonify({"erro": "Dados inválidos."}), 400
    