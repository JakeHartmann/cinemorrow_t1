

class TituloDuplicadoException(Exception):
    def __init__(self):
        self.mensagem = "Este título já está em uso."
