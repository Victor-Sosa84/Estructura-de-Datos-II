"""Modelo que representa un nodo de un arbol de expresion."""


class Nodo:
    """Nodo de un arbol binario de expresion.

    Puede representar un operando (nodo hoja, sin hijos) o un
    operador (nodo interno, con hijo izquierdo y derecho).

    Attributes:
        valor (str): Valor almacenado en el nodo (operando u
            operador).
        izquierda (Nodo | None): Hijo izquierdo del nodo.
        derecha (Nodo | None): Hijo derecho del nodo.
    """

    def __init__(self, valor, izquierda=None, derecha=None):
        """Inicializa el nodo con su valor e hijos opcionales.

        Args:
            valor (str): Valor del nodo (operando u operador).
            izquierda (Nodo, optional): Hijo izquierdo. Por defecto
                None.
            derecha (Nodo, optional): Hijo derecho. Por defecto
                None.
        """
        self.valor = valor
        self.izquierda = izquierda
        self.derecha = derecha

    def es_hoja(self):
        """Indica si el nodo es una hoja (sin hijos).

        Returns:
            bool: True si el nodo no tiene hijos, False en caso
            contrario.
        """
        return self.izquierda is None and self.derecha is None