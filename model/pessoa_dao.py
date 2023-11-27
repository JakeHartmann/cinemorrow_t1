from model.dao import DAO
from model.pessoa import Pessoa


class PessoaDAO(DAO):
    def __init__(self):
        super().__init__('pessoas.pkl')

    def add(self, pessoa: Pessoa):
        if isinstance(pessoa, Pessoa) and isinstance(pessoa.email, str):
            super().add(pessoa.email, pessoa)

    def get(self, email: str):
        if isinstance(email, str):
            return super().get(email)

    def remove(self, email: str):
        if isinstance(email, str):
            super().remove(email)
