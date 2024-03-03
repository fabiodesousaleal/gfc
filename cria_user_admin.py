from models.curso_model import CursoModel
from data.conexao import get_conexao
import sqlite3
from werkzeug.security import generate_password_hash

username = "admin"
senha = "senhafacil"
hashed_password = generate_password_hash(senha, method='pbkdf2:sha256')
con = get_conexao()
cursor = con.cursor()
cursor.execute('INSERT OR REPLACE INTO user (username, password, ativo) VALUES (?, ?, ?)', (username, hashed_password, 1))
con.commit()
con.close()
