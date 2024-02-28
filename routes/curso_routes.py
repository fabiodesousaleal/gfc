from flask import Blueprint, render_template, request, redirect, url_for
from models.curso_model import CursoModel
import sqlite3

curso_routes = Blueprint('curso_routes',__name__)
# Rota para a página de login

@curso_routes.route('/', methods=['GET', 'POST'])
def curso_listar():
    cursos = CursoModel.get_cursos()
    return render_template('cursos_listar.html', cursos=cursos)
