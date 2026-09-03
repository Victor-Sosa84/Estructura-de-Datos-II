class Nodo:
    def __init__(self, valor, izquierda=None, derecha=None):
        self.valor = valor
        self.izquierda = izquierda
        self.derecha = derecha

    def es_hoja(self):
        return self.izquierda is None and self.derecha is None