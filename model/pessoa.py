from midia import Midia


class Pessoa():
    def __init__(self, nome: str, email: str, midia_fav: Midia):
        if isinstance(nome, str):
            self.__nome = nome

        if isinstance(email, str):
            self.__email = email

        if isinstance(midia_fav, Midia):
            self.__midia_fav = midia_fav
        elif isinstance(midia_fav, None):
            print("Usuário escolheu deixar Mídia Favorita como vazia")

    @property
    def nome(self):
        if self.__nome is not None:
            return self.__nome

    @nome.setter
    def nome(self, nome):
        if isinstance(nome, str):
            self.__nome = nome

    @property
    def email(self):
        if self.__email is not None:
            return self.__email

    @email.setter
    def email(self, email):
        if isinstance(email, str):
            self.__email = email

    @property
    def midia_fav(self):
        if self.__midia_fav is not None:
            return self.__midia_fav

    @midia_fav.setter
    def midia_fav(self, midia_fav):
        if isinstance(midia_fav, Midia):
            self.__midia_fav = midia_fav
