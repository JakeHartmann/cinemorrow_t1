from model.midia import Midia
from datetime import datetime
from model.pessoa import Pessoa


class Grupo():

	def __init__(self, nome: str, integrante: Pessoa, midia_associada: Midia, data: datetime):
		self.__pessoas = []

		if isinstance(nome, str):
			self.__nome = nome

		if isinstance(integrante, Pessoa):
			self.__integrante = integrante
			self.__pessoas.append(integrante)

		if isinstance(midia_associada, Midia):
			self.__midia_associada = midia_associada

		if isinstance(data, datetime):
			self.__data = data

	@property
	def nome(self):
		return self.__nome

	@nome.setter
	def nome(self, nome):
		if isinstance(nome, str):
			self.__nome = nome

	@property
	def pessoas(self):
		return self.__pessoas

	@property
	def midia_associada(self):
		return self.__midia_associada

	@midia_associada.setter
	def midia_associada(self, midia_associada):
		if isinstance(midia_associada, Midia):
			self.__midia_associada = midia_associada

	@property
	def data(self):
		return self.__data

	@data.setter
	def data(self, data):
		if isinstance(data, datetime):
			self.__data = data
