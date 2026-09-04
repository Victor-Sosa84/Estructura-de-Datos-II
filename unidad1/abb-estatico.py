"""
titulo: Árbol Binario de Búsqueda (ABB) Estático
nombre: Victor David Sosa Coca
fecha: 20/08/2026
version: 1.0
"""


class ArbolTableroEstatico:
    """Árbol Binario que representa el tablero 3x3 de tres en raya de
    forma estática, usando un array de tamaño fijo en vez de nodos
    con punteros.

    Las posiciones del tablero se numeran así:
        0 | 1 | 2
        3 | 4 | 5
        6 | 7 | 8

    La relación entre nodos se calcula matemáticamente a partir del
    índice de cada posición dentro del array:
        hijo_izquierdo(i) = 2*i + 1
        hijo_derecho(i)   = 2*i + 2
        padre(i)          = (i - 1) // 2
    """

    TAMANIO = 9

    def __init__(self):
        """Inicializa el árbol con las 9 casillas del tablero vacías."""
        self._arbol = [None] * self.TAMANIO

    @property
    def arbol(self) -> list:
        """Getter del array completo que representa el tablero.

        Returns:
            list: Lista de 9 elementos (None, "X" u "O").
        """
        return self._arbol

    @arbol.setter
    def arbol(self, nuevo_arbol: list):
        """Setter del array completo del tablero, valida su tamaño.

        Args:
            nuevo_arbol (list): Nueva lista de 9 elementos a asignar.

        Raises:
            ValueError: Si la lista no tiene exactamente 9 elementos.
        """
        if len(nuevo_arbol) != self.TAMANIO:
            raise ValueError("El tablero debe tener exactamente 9 "
                            "posiciones.")
        self._arbol = nuevo_arbol

    @staticmethod
    def hijo_izquierdo(indice: int) -> int:
        """Calcula el índice del hijo izquierdo de una posición.

        Args:
            indice (int): Índice del nodo padre.

        Returns:
            int: Índice del hijo izquierdo.
        """
        return 2 * indice + 1

    @staticmethod
    def hijo_derecho(indice: int) -> int:
        """Calcula el índice del hijo derecho de una posición.

        Args:
            indice (int): Índice del nodo padre.

        Returns:
            int: Índice del hijo derecho.
        """
        return 2 * indice + 2

    @staticmethod
    def padre(indice: int) -> int:
        """Calcula el índice del nodo padre de una posición.

        Args:
            indice (int): Índice del nodo hijo.

        Returns:
            int: Índice del nodo padre. Si el índice es 0 (raíz),
                el resultado no tiene un padre válido.
        """
        return (indice - 1) // 2

    def _validar_posicion(self, posicion: int):
        """Valida que una posición esté dentro del rango del tablero.

        Args:
            posicion (int): Posición a validar (0-8).

        Raises:
            ValueError: Si la posición está fuera del rango 0-8.
        """
        if not 0 <= posicion < self.TAMANIO:
            raise ValueError("La posición debe estar entre 0 y 8.")

    def obtener_valor(self, posicion: int) -> str:
        """Obtiene el valor almacenado en una posición del tablero.

        Args:
            posicion (int): Posición de la casilla a consultar (0-8).

        Returns:
            str: Contenido de la casilla (None, "X" u "O").
        """
        self._validar_posicion(posicion)
        return self._arbol[posicion]

    def actualizar_valor(self, posicion: int, valor: str):
        """Actualiza el valor (jugada) de una casilla del tablero.

        Args:
            posicion (int): Posición de la casilla a actualizar (0-8).
            valor (str): Nuevo valor a colocar ("X" u "O").

        Raises:
            ValueError: Si el valor no es None, "X" ni "O".
        """
        if valor not in (None, "X", "O"):
            raise ValueError('El valor debe ser None, "X" u "O".')
        self._validar_posicion(posicion)
        self._arbol[posicion] = valor

    def obtener_hijos(self, posicion: int) -> tuple:
        """Obtiene los valores de los hijos izquierdo y derecho de una
        posición, calculados matemáticamente sobre el array.

        Args:
            posicion (int): Posición del nodo padre (0-8).

        Returns:
            tuple: Par (valor_izquierdo, valor_derecho). Cada elemento
                es None si esa posición no existe dentro del tablero.
        """
        indice_izq = self.hijo_izquierdo(posicion)
        indice_der = self.hijo_derecho(posicion)

        valor_izq = (self._arbol[indice_izq]
                    if indice_izq < self.TAMANIO else None)
        valor_der = (self._arbol[indice_der]
                    if indice_der < self.TAMANIO else None)
        return valor_izq, valor_der

    def obtener_tablero(self) -> list:
        """Devuelve una copia del estado actual del tablero.

        Returns:
            list: Lista de 9 elementos (None, "X" u "O") en orden de
                posición (0-8).
        """
        return list(self._arbol)


if __name__ == "__main__":
    # Se crea el tablero estático, con sus 9 casillas vacías de entrada
    arbol_estatico = ArbolTableroEstatico()

    # Se simulan algunas jugadas (mismas posiciones que en la versión
    # dinámica, para comparar resultados)
    arbol_estatico.actualizar_valor(4, "X")  # centro
    arbol_estatico.actualizar_valor(0, "O")  # esquina superior izquierda
    arbol_estatico.actualizar_valor(8, "X")  # esquina inferior derecha

    # Prueba de consulta directa de una casilla puntual
    print(f"Casilla 4 -> valor: {arbol_estatico.obtener_valor(4)}")

    # Prueba de obtención de los hijos de la raíz (posición 0)
    izquierdo, derecho = arbol_estatico.obtener_hijos(0)
    print(f"Hijos de la posición 0 -> izquierdo: {izquierdo}, "
        f"derecho: {derecho}")

    # Prueba de obtención del tablero completo como lista de 9 elementos
    print("Tablero actual:", arbol_estatico.obtener_tablero())