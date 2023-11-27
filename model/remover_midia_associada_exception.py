

class RemoverMidiaAssociadaException(Exception):
    def __init__(self):
        self.mensagem = "Essa mídia está associada a um grupo."
