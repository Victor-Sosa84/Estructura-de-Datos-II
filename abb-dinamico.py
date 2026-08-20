"""
titulo: Árbol Binario de Búsqueda (ABB) Dinámico
nombre: Victor David Sosa Coca
fecha: 20/08/2026
version: 1.0
"""


class Nodo:
    """Representa una casilla del tablero de tres en raya dentro del ABB.

    Cada nodo guarda la posición de la casilla (0 a 8, usada como
    criterio de comparación del árbol) y el valor que contiene
    (None, "X" u "O").
    """

    def __init__(self, posicion: int, valor: str = None):
        """Inicializa un nodo con su posición y valor iniciales.

        Args:
            posicion (int): Posición de la casilla en el tablero (0-8).
                Es el criterio usado para ordenar el árbol.
            valor (str): Contenido de la casilla. Puede ser None
                (casilla vacía), "X" u "O".
        """
        self.posicion = posicion
        self.valor = valor
        self.izquierda = None
        self.derecha = None

    @property
    def posicion(self) -> int:
        """Getter de la posición del nodo.

        Returns:
            int: Posición de la casilla (0-8).
        """
        return self._posicion

    @posicion.setter
    def posicion(self, nueva_posicion: int):
        """Setter de la posición del nodo, valida el rango del tablero.

        Args:
            nueva_posicion (int): Nueva posición a asignar (0-8).

        Raises:
            ValueError: Si la posición está fuera del rango 0-8.
        """
        if not 0 <= nueva_posicion <= 8:
            raise ValueError("La posición debe estar entre 0 y 8.")
        self._posicion = nueva_posicion

    @property
    def valor(self) -> str:
        """Getter del valor almacenado en la casilla.

        Returns:
            str: Contenido de la casilla (None, "X" u "O").
        """
        return self._valor

    @valor.setter
    def valor(self, nuevo_valor: str):
        """Setter del valor de la casilla, valida que sea None, "X" u "O".

        Args:
            nuevo_valor (str): Nuevo valor a asignar a la casilla.

        Raises:
            ValueError: Si el valor no es None, "X" ni "O".
        """
        if nuevo_valor not in (None, "X", "O"):
            raise ValueError('El valor debe ser None, "X" u "O".')
        self._valor = nuevo_valor


class ArbolTablero:
    """Árbol Binario de Búsqueda que representa el tablero 3x3 de tres
    en raya de forma dinámica (nodos conectados mediante referencias).

    Las posiciones del tablero se numeran así:
        0 | 1 | 2
        3 | 4 | 5
        6 | 7 | 8

    Los nodos se ordenan comparando la posición (no el valor de la
    casilla), de modo que el árbol siga siendo un ABB válido.
    """

    def __init__(self):
        """Inicializa el árbol del tablero sin ninguna casilla cargada."""
        self.raiz = None

    def insertar(self, posicion: int, valor: str = None):
        """Inserta una nueva casilla en el árbol según su posición.

        Args:
            posicion (int): Posición de la casilla a insertar (0-8).
            valor (str): Contenido inicial de la casilla (None, "X" u
                "O").
        """
        if self.raiz is None:
            self.raiz = Nodo(posicion, valor)
        else:
            self._insertar_recursivo(self.raiz, posicion, valor)

    def _insertar_recursivo(self, nodo_actual: Nodo, posicion: int,
                            valor: str):
        """Recorre el árbol comparando posiciones hasta insertar el
        nuevo nodo en el lugar que corresponde.

        Args:
            nodo_actual (Nodo): Nodo desde el que se sigue comparando.
            posicion (int): Posición de la casilla a insertar.
            valor (str): Contenido inicial de la casilla.
        """
        if posicion < nodo_actual.posicion:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = Nodo(posicion, valor)
            else:
                self._insertar_recursivo(nodo_actual.izquierda, posicion,
                                        valor)
        elif posicion > nodo_actual.posicion:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = Nodo(posicion, valor)
            else:
                self._insertar_recursivo(nodo_actual.derecha, posicion,
                                        valor)
        # Si la posición ya existe, no se duplica el nodo.

    def buscar(self, posicion: int) -> Nodo:
        """Busca el nodo correspondiente a una posición del tablero.

        Args:
            posicion (int): Posición de la casilla a buscar (0-8).

        Returns:
            Nodo: El nodo encontrado, o None si la posición no existe
                en el árbol.
        """
        return self._buscar_recursivo(self.raiz, posicion)

    def _buscar_recursivo(self, nodo_actual: Nodo, posicion: int) -> Nodo:
        """Recorre el árbol comparando posiciones hasta encontrar el
        nodo buscado.

        Args:
            nodo_actual (Nodo): Nodo desde el que se sigue comparando.
            posicion (int): Posición de la casilla a buscar.

        Returns:
            Nodo: El nodo encontrado, o None si no existe.
        """
        if nodo_actual is None or nodo_actual.posicion == posicion:
            return nodo_actual
        if posicion < nodo_actual.posicion:
            return self._buscar_recursivo(nodo_actual.izquierda, posicion)
        return self._buscar_recursivo(nodo_actual.derecha, posicion)

    def actualizar_valor(self, posicion: int, valor: str) -> bool:
        """Actualiza el valor (jugada) de una casilla ya existente.

        Args:
            posicion (int): Posición de la casilla a actualizar (0-8).
            valor (str): Nuevo valor a colocar ("X" u "O").

        Returns:
            bool: True si la casilla existía y se actualizó, False si
                no se encontró esa posición en el árbol.
        """
        nodo = self.buscar(posicion)
        if nodo is None:
            return False
        nodo.valor = valor
        return True

    def obtener_tablero(self) -> list:
        """Recorre el árbol y arma una lista de 9 posiciones con los
        valores actuales de cada casilla, en orden de posición (0-8).

        Returns:
            list: Lista de 9 elementos (None, "X" u "O") representando
                el estado actual del tablero.
        """
        tablero = [None] * 9
        self._llenar_tablero(self.raiz, tablero)
        return tablero

    def _llenar_tablero(self, nodo_actual: Nodo, tablero: list):
        """Recorre el árbol en inorden y va llenando la lista del
        tablero según la posición de cada nodo.

        Args:
            nodo_actual (Nodo): Nodo actual del recorrido.
            tablero (list): Lista de 9 posiciones que se va llenando.
        """
        if nodo_actual is None:
            return
        self._llenar_tablero(nodo_actual.izquierda, tablero)
        tablero[nodo_actual.posicion] = nodo_actual.valor
        self._llenar_tablero(nodo_actual.derecha, tablero)


if __name__ == "__main__":
    # Se crean las 9 casillas del tablero (posiciones 0 a 8, vacías)
    arbol = ArbolTablero()
    for i in range(9):
        arbol.insertar(i)

    # Se simulan algunas jugadas
    arbol.actualizar_valor(4, "X")  # centro
    arbol.actualizar_valor(0, "O")  # esquina superior izquierda
    arbol.actualizar_valor(8, "X")  # esquina inferior derecha

    # Prueba de búsqueda de una casilla puntual
    nodo_encontrado = arbol.buscar(4)
    print(f"Casilla 4 -> valor: {nodo_encontrado.valor}")

    # Prueba de obtención del tablero completo como lista de 9 elementos
    print("Tablero actual:", arbol.obtener_tablero())