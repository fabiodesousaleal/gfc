from data.conexao import get_conexao

class ClasseBase:
    tabela = None

    def save(self):
        if not self.tabela:
            raise ValueError("Nome da tabela não especificado na classe derivada.")

        con = get_conexao()
        cursor = con.cursor()

        if self.id is None:
            columns = ', '.join(self.__dict__.keys())
            placeholders = ', '.join(['?' for _ in range(len(self.__dict__))])
            values = tuple(self.__dict__.values())
            query = f'INSERT INTO {self.tabela} ({columns}) VALUES ({placeholders})'
        else:
            set_clause = ', '.join([f'{key}=?' for key in self.__dict__.keys()])
            values = tuple(self.__dict__.values()) + (self.id,)
            query = f'UPDATE {self.tabela} SET {set_clause} WHERE id=?'

        cursor.execute(query, values)
        con.commit()
        con.close()

    
    def delete(self):
        if not self.tabela or self.id is None:
            raise ValueError("Nome da tabela não especificado na classe derivada ou ID não fornecido.")

        con = get_conexao()
        cursor = con.cursor()

        query = f'DELETE FROM {self.tabela} WHERE id=?'
        cursor.execute(query, (self.id,))

        con.commit()
        con.close()

    def to_dict(self, *args):
        if not args:
            args = self.__dict__.keys()
        return {attr: getattr(self, attr) for attr in args}   
    
   
    @classmethod
    def get_all(cls):
        if not cls.tabela:
            raise ValueError("Nome da tabela não especificado na classe derivada.")

        con = get_conexao()
        cursor = con.cursor()

        query = f'SELECT * FROM {cls.tabela}'
        cursor.execute(query)

        colunas = [coluna[0] for coluna in cursor.description]
        objetos = [cls(**dict(zip(colunas, row))) for row in cursor.fetchall()]

        con.close()
        return objetos


    @classmethod
    def get_by_id(cls, obj_id):
        if not cls.tabela:
            raise ValueError("Nome da tabela não especificado na classe derivada.")

        con = get_conexao()
        cursor = con.cursor()

        query = f'SELECT * FROM {cls.tabela} WHERE id=?'
        cursor.execute(query, (obj_id,))

        colunas = [coluna[0] for coluna in cursor.description]
        row = cursor.fetchone()

        if row:
            objeto = cls(**dict(zip(colunas, row)))
        else:
            objeto = None

        con.close()
        return objeto

    
    @staticmethod
    def serialize(itens):
        serialized_list = []
        for item in itens:
            serialized_list.append(item.to_dict())
        return serialized_list 

    