from flask import Flask, Blueprint, redirect
from flask_login import LoginManager, login_required
from routes.ficha_routes import ficha_routes
from routes.login_routes import login_routes
from routes.curso_routes import curso_routes
from routes.tipo_trabalho_routes import tt_routes
from routes.campus_routes import campus_routes
from routes.parametro_routes import parametro_routes
from models.user_model import UserModel
from utils.utils import criar_login
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

login_manager = LoginManager(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'asdçlkskasdbbidkjçadkj56çlkjsdlçk326362324gsh467s')


@login_manager.user_loader
def load_user(user_id):
    return UserModel.get_user_by_id(user_id)



app.register_blueprint(ficha_routes, url_prefix='/ficha')
app.register_blueprint(login_routes, url_prefix='/login')
app.register_blueprint(curso_routes, url_prefix='/cursos')
app.register_blueprint(tt_routes, url_prefix='/tipo_trabalho')
app.register_blueprint(campus_routes, url_prefix='/campus')
app.register_blueprint(parametro_routes, url_prefix='/parametro')

login_manager.login_view = 'login_routes.home'


@app.route('/')
def index():
    return redirect('/ficha/', code=302)

def createuser(user, password):
    criar_login(user, password)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
