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
		return self.__titulo

	@titulo.setter
	def titulo(self, titulo):
		if isinstance(titulo, str):
			self.__titulo = titulo

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
