# campus_model.py
import sqlite3
from data.conexao import get_conexao
from .base_model import ClasseBase

class CampusModel(ClasseBase):
    tabela = "campus"
    def __init__(self, nome, ativo=1, id=None):
        self.id = id
        self.nome = nome
        self.ativo = ativo
    
    def __str__(self) -> str:
        return self.nome