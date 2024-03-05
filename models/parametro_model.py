from .base_model import ClasseBase

class ParametroModel(ClasseBase):
    tabela = "parametro"
    def __init__(self, instituicao, cabecalho1, cabecalho2, cabecalho3, rodape, id=None) -> None:
        self.id = id
        self.instituicao = instituicao
        self.cabecalho1 = cabecalho1
        self.cabecalho2 = cabecalho2
        self.cabecalho3 = cabecalho3
        self.rodape = rodape
    

    