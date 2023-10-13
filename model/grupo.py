from midia import Midia
from datetime import datetime
from pessoa import Pessoa


class Grupo():

    def __init__(self, titulo: str, integrante: Pessoa, midia_associada: Midia, data: datetime):
        self.__pessoas = []

        if isinstance(titulo, str):
            self.__titulo = titulo

        if isinstance(integrante, Pessoa):
            self.__integrante = integrante
            self.__pessoas.append(integrante)

        if isinstance(midia_associada, Midia):
            self.__midia_associada = midia_associada

        if isinstance(data, datetime):
            self.__data = data

    @property
    def titulo(self):
        if self.__titulo is not None:
            return self.__titulo

    def titulo(self, titulo):
        if isinstance(titulo, str):
            self.__titulo = titulo

    @property
    def pessoas(self):
        if self.__pessoas:
            return self.__pessoas

    @property
    def midia_associada(self):
        if self.__midia_associada is not None:
            return self.__midia_associada

    def midia_associada(self, midia_associada):
        if isinstance(midia_associada, Midia):
            self.__midia_associada = midia_associada

    @property
    def data(self):
        if self.__data is not None:
            return self.__data

    def data(self, data):
        if isinstance(data, datetime):
            self.__data = data
