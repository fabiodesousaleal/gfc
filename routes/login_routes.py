from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import check_password_hash

login_routes = Blueprint('login_routes',__name__)

# Rota para a página de login
@login_routes.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('data/gfc.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
        user = cursor.fetchone()

        conn.close()

        # Verifica se o usuário existe e a senha está correta
        if user and check_password_hash(user[2], password):
            return 'Login bem-sucedido!'
        else:
            return render_template('home.html')


    return render_template('login.html')
