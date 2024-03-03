from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash

from models.user_model import UserModel

login_routes = Blueprint('login_routes', __name__)

@login_routes.route('/', methods=['GET'])
def home():
    return render_template('login.html')

@login_routes.route('/autenticar', methods=['POST'])
def logar():
    dados = request.form.to_dict()
    username = dados['username']
    password = dados['password']

    user = UserModel.check_login(username, password)

    if user:
        login_user(user)
        return redirect(url_for('curso_routes.curso_listar'))  # Use o nome da função da rota desejada

    return render_template('login.html', mensagem='Usuário ou Senha incorretos')

@login_routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_routes.home'))

