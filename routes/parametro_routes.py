
from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required
from models.parametro_model import ParametroModel


parametro_routes = Blueprint('parametro_routes',__name__)


@parametro_routes.route('/', methods=['GET', 'POST'])
@login_required
def parametro_listar():
    parametros = ParametroModel.get_all()   
    return render_template('parametro_view.html', parametros = parametros )


@parametro_routes.route('/save', methods=['POST'])
def save_parametro():
    success_message = None
    error_message = None

    if request.method == 'POST':
        dados = request.form.to_dict()
        id = dados.get('parametro_id')

        try:
            if id:
                parametro = ParametroModel.get_by_id(id)
                if parametro:
                    parametro.instituicao = dados.get('instituicao')
                    parametro.cabecalho1 = dados.get('cabecalho1')
                    parametro.cabecalho2 = dados.get('cabecalho2')
                    parametro.cabecalho3 = dados.get('cabecalho3')
                    parametro.rodape = dados.get('rodape')                                   
                    
                    success_message = 'parametros atualizado com sucesso!'
                else:
                    error_message = 'parametro não encontrado'
            else:
                parametro = ParametroModel(
                    instituicao = dados.get('instituicao'),
                    cabecalho1 = dados.get('cabecalho1'),
                    cabecalho2 = dados.get('cabecalho2'),
                    cabecalho3 = dados.get('cabecalho3'),
                    rodape = dados.get('rodape')
                )

                success_message = 'Tipo Trabalho criado com sucesso!'

            parametro.save()
        except Exception as e:
            error_message = f'Erro ao salvar parametro: {str(e)}'

    parametros = ParametroModel.get_all()
    

    return render_template('parametro_view.html', parametros=parametros, success_message=success_message, error_message=error_message )


@parametro_routes.route('/editar', methods=["POST"])
@login_required
def busca_parametro():
    dados = request.get_json()
    parametro_id = dados.get("parametro_id")
    parametro = ParametroModel.get_by_id(parametro_id)
    if parametro:
        return jsonify(parametro.to_dict())
    else:
        return jsonify({"erro": "Dados inválidos."}), 400

