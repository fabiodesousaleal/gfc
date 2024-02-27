from flask import Flask, Blueprint, redirect
from routes.ficha_routes import ficha_routes
from routes.login_routes import login_routes
from routes.curso_routes import curso_routes

app = Flask(__name__)

app.register_blueprint(ficha_routes, url_prefix='/ficha')
app.register_blueprint(login_routes, url_prefix='/login')
app.register_blueprint(curso_routes, url_prefix='/cursos')

@app.route('/')
def index():
    return redirect('/ficha/', code=302)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
