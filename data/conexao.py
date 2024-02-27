import sqlite3


def get_conexao():
    conexao = sqlite3.connect('data/gfc.db')
    return conexao

def get_objeto_by_id(tabela, id):
    conn = get_conexao()
    cursor = conn.cursor()       
    query = f'SELECT * FROM {tabela} WHERE id = ?'
    cursor.execute(query, (id,))
    resultado = cursor.fetchone()
    conn.close()    
    return resultado
