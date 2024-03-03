import sqlite3
from data.conexao import get_conexao
from werkzeug.security import check_password_hash


class UserModel:
    def __init__(self, id, username, password, ativo=1):
        self.id = id
        self.username = username
        self.password = password
        self.ativo = ativo

    @staticmethod
    def get_user_by_id(user_id: int):
        con = get_conexao()
        cursor = con.cursor()
        query = 'SELECT * FROM user WHERE id=?'
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()

        if row:
            user = UserModel(
                id=row[0],
                username=row[1],
                password=row[2],
                ativo=row[3],
            )
            con.close()
            return user
        else:
            con.close()
            return None 
        
    
    @staticmethod
    def get_user_by_username(username: str):
        con = get_conexao()
        cursor = con.cursor()
        query = 'SELECT * FROM user WHERE username=?'
        cursor.execute(query, (username,))
        row = cursor.fetchone()

        if row:
            user = UserModel(
                id=row[0],
                username=row[1],
                password=row[2],
                ativo=row[3],
            )
            con.close()
            return user
        else:
            con.close()
            return None


    @staticmethod
    def check_login(username, password):
        con = get_conexao()
        cursor = con.cursor()

        cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
        user = cursor.fetchone()

        # Verifica se o usuário existe e a senha está correta
        if user and check_password_hash(user[2], password) and user[3] == 1:
            return UserModel(
                id=user[0],
                username=user[1],
                password=user[2],
                ativo=user[3],
            )
        else:
            return None
    
    
    @property
    def is_authenticated(self):
        return True if self.id is not None else False


    @property
    def is_active(self):
        return self.ativo == 1

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    
    
    def __str__(self) -> str:
        return self.nome