from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

curso_routes = Blueprint('curso_routes',__name__)
# Rota para a página de login

def buscar_cursos():
    conn = sqlite3.connect('data/gfc.db')  # Certifique-se de ajustar o caminho do seu banco de dados
    cursor = conn.cursor()

    # Consulta para obter informações sobre cursos
    cursor.execute('SELECT id, nome, cdd, campus_id, tipo, ativo FROM curso')
    cursos = cursor.fetchall()

    conn.close()

    return cursos

@curso_routes.route('/', methods=['GET', 'POST'])
def curso_listar():
    cursos = buscar_cursos()
    return render_template('cursos_listar.html', cursos=cursos)
