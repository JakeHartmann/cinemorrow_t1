from abc import ABC, abstractmethod
import os
import PySimpleGUI as sg


class AbstractTela(ABC):
    @abstractmethod
    def __init__(self):
        super().__init__()
        self.__window = None
        self.init_components()

    def open(self):
        button, values = self.__window.Read()
        return button, values

    def close(self):
        self.__window.Close()

    def show_message(self, titulo: str, mensagem: str):
        sg.Popup(titulo, mensagem)

    @abstractmethod
    def init_components(self):
        pass

    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, window):
        self.__window = window

    def output_texto(self, texto):
        print(texto)
