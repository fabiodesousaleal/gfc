from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from flask_login import login_required
from models.campus_model import CampusModel


campus_routes = Blueprint('campus_routes',__name__)


@campus_routes.route('/', methods=['GET', 'POST'])
@login_required
def campus_listar():
    campus = CampusModel.get_all()   
    return render_template('campus_view.html', campus = campus )


@campus_routes.route('/save', methods=['POST'])
def save_campus():
    success_message = None
    error_message = None

    if request.method == 'POST':
        dados = request.form.to_dict()
        id = dados.get('campus_id')

        try:
            if id:
                campus = CampusModel.get_by_id(id)
                if campus:
                    campus.nome = dados.get('nome')                                    
                    campus.ativo = dados.get('ativo')
                    success_message = 'campus atualizado com sucesso!'
                else:
                    error_message = 'campus não encontrado'
            else:
                campus = CampusModel(
                    nome=dados.get('nome'),                    
                    ativo=dados.get('ativo')
                )

                success_message = 'Campus criado com sucesso!'

            campus.save()
        except Exception as e:
            error_message = f'Erro ao salvar campus: {str(e)}'

    campus = CampusModel.get_all()
    

    return render_template('campus_view.html', campus=campus, success_message=success_message, error_message=error_message )


@campus_routes.route('/editar', methods=["POST"])
@login_required
def busca_campus():
    dados = request.get_json()
    campus_id = dados.get("campus_id")
    campus = CampusModel.get_by_id(campus_id)
    if campus:
        return jsonify(campus.to_dict())
    else:
        return jsonify({"erro": "Dados inválidos."}), 400


@campus_routes.route('/delete', methods=["POST"])
@login_required
def remove_campus():
    dados = request.get_json()
    campus_id = dados.get("id")
    campus = CampusModel.get_by_id(campus_id)
    if campus:
        campus.delete()
        return jsonify({"mensagem": "Removido com sucesso"})
    else:
        return jsonify({"erro": "Dados inválidos."}), 400
    