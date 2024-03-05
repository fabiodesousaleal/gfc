import sqlite3
from werkzeug.security import generate_password_hash
import csv

DEFAULT_ADMIN = 'admin'
DEFAULT_PASSWORD = 'admin'

INSTITUICAO ='Universidade Federal do Norte do Tocantins'   
CABECALHO1 = "Dados Internacionais de Catalogação na Publicação (CIP)"
CABECALHO2 = "Sistema de Geração de Ficha Catalografica SGFC-UFNT" 
CABECALHO3 = "Gerado automaticamente mediante os dados fornecidos pelo(a) autor(a)"

RODAPE = "TODOS OS DIREITOS RESERVADOS – A reprodução total ou parcial, de qualquer forma ou por qualquer meio deste documento é autorizado desde que citada a fonte. A violação dos direitos do autor (Lei nº 9.610/98) é crime estabelecido pelo artigo 184 do Código Penal."


def create_table():
    try:    
        conn = sqlite3.connect('data/gfc.db')
        cursor = conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    ativo INTEGER DEFAULT 1
                )
            ''')
        
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS campus (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,                        
                    ativo INTEGER DEFAULT 1
                )
                ''') 

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS curso (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cdd TEXT NOT NULL,
                campus_id INTEGER,
                tipo TEXT NOT NULL,
                ativo INTEGER DEFAULT 1,
                FOREIGN KEY (campus_id) REFERENCES campus(id) ON DELETE CASCADE       
                
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tipo_trabalho (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,           
                ativo INTEGER DEFAULT 1            
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS curso_tipo_trabalho (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                curso_id INTEGER,            
                tipo_trabalho_id INTEGER,            
                FOREIGN KEY (curso_id) REFERENCES curso(id)
                FOREIGN KEY (tipo_trabalho_id) REFERENCES tipo_trabalho(tipo_trabalho_id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parametro (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                instituicao TEXT,
                cabecalho1 TEXT,
                cabecalho2 TEXT,
                cabecalho3 TEXT,
                rodape TEXT        
            )
        ''')        

        cursor.execute('INSERT OR REPLACE INTO parametro (instituicao, cabecalho1, cabecalho2, cabecalho3, rodape) VALUES (?, ?, ?, ?, ?)', (INSTITUICAO, CABECALHO1, CABECALHO2, CABECALHO3, RODAPE))

        path_campus = 'data/campus.csv'
        with open(path_campus, 'r', newline='', encoding='utf-8') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv, delimiter=',')
            for linha in leitor_csv:        
                nome = linha[0]
                cursor.execute('INSERT OR REPLACE INTO campus (nome, ativo) VALUES (?, ?)', (nome, 1))    
            
        
        path_cursos = 'data/cursos.csv'
        with open(path_cursos, 'r', newline='', encoding='utf-8') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv, delimiter=',')
            for linha in leitor_csv:        
                nome = linha[0]
                campus_id = linha[1]
                tipo = linha[2]
                cdd = linha[3]
                cursor.execute('INSERT OR REPLACE INTO curso (nome, cdd, campus_id, tipo, ativo) VALUES (?, ?, ?, ?, ?)', (nome, cdd, campus_id, tipo, 1))
            

        path_cursos = 'data/tipo_trabalho.csv'
        with open(path_cursos, 'r', newline='', encoding='utf-8') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv, delimiter=',')
            for linha in leitor_csv:        
                nome = linha[0]           
                cursor.execute('INSERT OR REPLACE INTO tipo_trabalho (nome, ativo) VALUES (?, ?)', (nome, 1))
            
        
        hashed_password = generate_password_hash(DEFAULT_PASSWORD, method='pbkdf2:sha256')
        cursor.execute('INSERT OR REPLACE INTO user (username, password, ativo) VALUES (?, ?, ?)', (DEFAULT_ADMIN, hashed_password, 1))
        
        conn.commit()
        conn.close()        
    
    except Exception as e:
        print(f"Erro durante a criação do banco de dados: {e}")
        conn.rollback()
    
    finally:
        conn.close()

create_table()