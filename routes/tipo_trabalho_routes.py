from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from flask_login import login_required
from models.tipo_trabalho_model import TipoTrabalhoModel


tt_routes = Blueprint('tt_routes',__name__)


@tt_routes.route('/', methods=['GET', 'POST'])
@login_required
def tipo_trabalho_listar():
    tipos_trabalhos = TipoTrabalhoModel.get_all()   
    return render_template('tipo_trabalho_view.html', tipos_trabalhos = tipos_trabalhos )


@tt_routes.route('/save', methods=['POST'])
def save_tipo_trabalho():
    success_message = None
    error_message = None

    if request.method == 'POST':
        dados = request.form.to_dict()
        id = dados.get('tipo_trabalho_id')

        try:
            if id:
                tipo_trabalho = TipoTrabalhoModel.get_by_id(id)
                if tipo_trabalho:
                    tipo_trabalho.nome = dados.get('nome')                                    
                    tipo_trabalho.ativo = dados.get('ativo')
                    success_message = 'Tipo_trabalho atualizado com sucesso!'
                else:
                    error_message = 'Tipo_trabalho não encontrado'
            else:
                tipo_trabalho = TipoTrabalhoModel(
                    nome=dados.get('nome'),                    
                    ativo=dados.get('ativo')
                )

                success_message = 'Tipo Trabalho criado com sucesso!'

            tipo_trabalho.save()
        except Exception as e:
            error_message = f'Erro ao salvar tipo_trabalho: {str(e)}'

    tipos_trabalhos = TipoTrabalhoModel.get_tipos_trabalho()
    

    return render_template('tipo_trabalho_view.html', tipos_trabalhos=tipos_trabalhos, success_message=success_message, error_message=error_message )


@tt_routes.route('/editar', methods=["POST"])
@login_required
def teste():
    dados = request.get_json()
    tipo_trabalho_id = dados.get("tipo_trabalho_id")
    tipo_trabalho = TipoTrabalhoModel.get_by_id(tipo_trabalho_id)
    if tipo_trabalho:
        return jsonify(tipo_trabalho.to_dict())
    else:
        return jsonify({"erro": "Dados inválidos."}), 400
    