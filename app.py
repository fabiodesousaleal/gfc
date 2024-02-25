from flask import Flask, Blueprint, redirect
from routes.ficha_routes import ficha_routes

app = Flask(__name__)

app.register_blueprint(ficha_routes, url_prefix='/ficha')

@app.route('/')
def index():
    return redirect('/ficha/', code=302)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
