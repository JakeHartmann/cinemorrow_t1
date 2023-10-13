from abc import ABC, abstractmethod


class Midia(ABC):
    @abstractmethod
    def __init__(self, titulo: str):
        if isinstance(titulo, str):
            self.__titulo = titulo
        
    @property
    def titulo(self):
        if self.__titulo is not None:
            return self.__titulo

    @titulo.setter
    def titulo(self, titulo):
        if isinstance(titulo, str):
            self.__titulo = titulo
