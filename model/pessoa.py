from model.midia import Midia


class Pessoa():
    def __init__(self, nome: str, email: str, midia_fav = None):
        if isinstance(nome, str):
            self.__nome = nome

        if isinstance(email, str):
            self.__email = email

        if isinstance(midia_fav, str):
            self.__midia_fav = midia_fav
        elif midia_fav is None:
            self.__midia_fav = None

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        if isinstance(nome, str):
            self.__nome = nome

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        if isinstance(email, str):
            self.__email = email

    @property
    def midia_fav(self):
        if self.__midia_fav is not None:
            return self.__midia_fav
        elif self.__midia_fav is None:
            return "Nenhuma"

    @midia_fav.setter
    def midia_fav(self, midia_fav):
        if isinstance(midia_fav, str):
            self.__midia_fav = midia_fav
