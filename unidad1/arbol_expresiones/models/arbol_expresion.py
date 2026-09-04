"""Modelo que representa un arbol binario de expresion aritmetica.

Construye el arbol a partir de una expresion infija utilizando el
metodo de las dos pilas (operandos y operadores), y permite obtener
las representaciones prefija y postfija mediante los recorridos
preorden y postorden respectivamente.
"""

from models.nodo import Nodo


class ArbolExpresion:
    """Arbol binario construido a partir de una expresion infija.

    Attributes:
        expresion (str): Expresion infija original, sin procesar.
        raiz (Nodo | None): Nodo raiz del arbol construido.
    """

    def __init__(self, expresion):
        """Inicializa el arbol construyendolo a partir de la expresion.

        Args:
            expresion (str): Expresion infija a convertir en arbol.
        """
        self.expresion = expresion
        self.raiz = self.construir_arbol(expresion)

    def precedencia(self, operador):
        """Devuelve la precedencia numerica de un operador.

        Args:
            operador (str): Operador a evaluar ('+', '-', '*', '/').

        Returns:
            int: 2 para '*' y '/', 1 para '+' y '-', 0 en otro caso.
        """
        if operador in ('+', '-'):
            return 1
        if operador in ('*', '/'):
            return 2
        return 0

    def construir_arbol(self, expresion):
        """Construye el arbol de expresion usando dos pilas.

        Recorre la expresion infija caracter por caracter. Los
        operandos se apilan como nodos hoja; los operadores se
        apilan respetando precedencia, resolviendo (armando
        subarboles) cuando corresponde.

        Args:
            expresion (str): Expresion infija a procesar.

        Returns:
            Nodo | None: Nodo raiz del arbol construido, o None
            si la expresion esta vacia.
        """
        pila_operandos = []
        pila_operadores = []

        def resolver():
            """Saca un operador y dos operandos, arma un subarbol
            y lo vuelve a apilar en la pila de operandos."""
            operador = pila_operadores.pop()
            derecha = pila_operandos.pop()
            izquierda = pila_operandos.pop()
            nodo = Nodo(operador, izquierda, derecha)
            pila_operandos.append(nodo)

        i = 0
        while i < len(expresion):
            caracter = expresion[i]

            if caracter == ' ':
                i += 1
                continue

            if caracter.isalnum():
                pila_operandos.append(Nodo(caracter))

            elif caracter == '(':
                pila_operadores.append(caracter)

            elif caracter == ')':
                while pila_operadores and pila_operadores[-1] != '(':
                    resolver()
                pila_operadores.pop()  # Descarta el '(' correspondiente.

            else:  # Operador (+, -, *, /)
                while (pila_operadores and pila_operadores[-1] != '(' and
                        self.precedencia(pila_operadores[-1]) >=
                        self.precedencia(caracter)):
                    resolver()
                pila_operadores.append(caracter)

            i += 1

        while pila_operadores:
            resolver()

        return pila_operandos[-1] if pila_operandos else None

    def preorden(self, nodo=None, resultado=None):
        """Recorre el arbol en preorden (raiz, izquierda, derecha).

        Este recorrido corresponde a la expresion prefija.

        Args:
            nodo (Nodo, optional): Nodo desde el cual continuar el
                recorrido. Si es None, comienza desde la raiz.
            resultado (list, optional): Lista acumuladora de valores.
                Si es None, se inicializa vacia.

        Returns:
            list: Lista de valores en orden preorden.
        """
        if resultado is None:
            resultado = []
            nodo = self.raiz
        if nodo:
            resultado.append(nodo.valor)
            self.preorden(nodo.izquierda, resultado)
            self.preorden(nodo.derecha, resultado)
        return resultado

    def postorden(self, nodo=None, resultado=None):
        """Recorre el arbol en postorden (izquierda, derecha, raiz).

        Este recorrido corresponde a la expresion postfija.

        Args:
            nodo (Nodo, optional): Nodo desde el cual continuar el
                recorrido. Si es None, comienza desde la raiz.
            resultado (list, optional): Lista acumuladora de valores.
                Si es None, se inicializa vacia.

        Returns:
            list: Lista de valores en orden postorden.
        """
        if resultado is None:
            resultado = []
            nodo = self.raiz
        if nodo:
            self.postorden(nodo.izquierda, resultado)
            self.postorden(nodo.derecha, resultado)
            resultado.append(nodo.valor)
        return resultado

    def obtener_prefija(self):
        """Obtiene la expresion prefija como texto.

        Returns:
            str: Valores del recorrido preorden separados por espacio.
        """
        return ' '.join(self.preorden())

    def obtener_postfija(self):
        """Obtiene la expresion postfija como texto.

        Returns:
            str: Valores del recorrido postorden separados por espacio.
        """
        return ' '.join(self.postorden())