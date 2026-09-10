"""
titulo: Arbol Binario de Busqueda con Balanceo (AVL)
nombre: Victor David Sosa Coca
fecha: 09/09/2026
version: 1.0
"""

from collections import deque


class Nodo:
    """Nodo de un arbol binario de busqueda balanceado.

    Attributes:
        valor: Valor almacenado en el nodo.
        izquierda (Nodo | None): Hijo izquierdo del nodo.
        derecha (Nodo | None): Hijo derecho del nodo.
        altura (int): Altura del nodo dentro del arbol, usada para
            calcular el factor de balance durante el balanceo AVL.
    """

    def __init__(self, valor):
        """Inicializa un nodo hoja con el valor dado.

        Args:
            valor: Valor a almacenar en el nodo.
        """
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1


class Arbol:
    """Arbol Binario de Busqueda con balanceo automatico (AVL)."""

    def __init__(self):
        """Inicializa un arbol vacio."""
        self._raiz = None

    # --- Utilidades de altura y balance ---

    def _altura_nodo(self, nodo):
        """Obtiene la altura almacenada de un nodo.

        Args:
            nodo (Nodo | None): Nodo a consultar.

        Returns:
            int: Altura del nodo, o 0 si el nodo es None.
        """
        if nodo is None:
            return 0
        return nodo.altura

    @property
    def altura(self):
        """Altura total del arbol (altura de la raiz).

        Returns:
            int: Altura del arbol, o 0 si esta vacio.
        """
        return self._altura_nodo(self._raiz)

    def nivel(self, valor):
        """Calcula la profundidad de un valor dentro del arbol.

        La raiz se considera de nivel 0.

        Args:
            valor: Valor a buscar.

        Returns:
            int | None: Nivel del valor, o None si no se encuentra.
        """
        nodo = self._raiz
        profundidad = 0
        while nodo is not None:
            if valor == nodo.valor:
                return profundidad
            if valor < nodo.valor:
                nodo = nodo.izquierda
            else:
                nodo = nodo.derecha
            profundidad += 1
        return None

    def factor_balance(self, nodo):
        """Calcula el factor de balance de un nodo.

        El factor se obtiene como la altura del subarbol izquierdo
        menos la altura del subarbol derecho. Un arbol AVL valido
        mantiene este factor entre -1 y 1 en todos sus nodos.

        Args:
            nodo (Nodo | None): Nodo a evaluar.

        Returns:
            int: Factor de balance del nodo, o 0 si es None.
        """
        if nodo is None:
            return 0
        return self._altura_nodo(nodo.izquierda) - self._altura_nodo(nodo.derecha)

    def _actualizar_altura(self, nodo):
        """Recalcula y guarda la altura de un nodo segun sus hijos.

        Args:
            nodo (Nodo): Nodo cuya altura se va a actualizar.
        """
        nodo.altura = 1 + max(
            self._altura_nodo(nodo.izquierda),
            self._altura_nodo(nodo.derecha),
        )

    # --- Rotaciones ---

    def rotacion_derecha(self, nodo):
        """Aplica una rotacion simple hacia la derecha.

        Se usa cuando un nodo esta desbalanceado hacia la izquierda.
        El hijo izquierdo del nodo pasa a ser la nueva raiz de este
        subarbol, y el nodo original baja como su hijo derecho.

        Args:
            nodo (Nodo): Nodo desbalanceado sobre el cual rotar.

        Returns:
            Nodo: Nueva raiz del subarbol tras la rotacion.
        """
        pivote = nodo.izquierda
        subarbol_temporal = pivote.derecha

        pivote.derecha = nodo
        nodo.izquierda = subarbol_temporal

        self._actualizar_altura(nodo)
        self._actualizar_altura(pivote)

        return pivote

    def rotacion_izquierda(self, nodo):
        """Aplica una rotacion simple hacia la izquierda.

        Se usa cuando un nodo esta desbalanceado hacia la derecha.
        El hijo derecho del nodo pasa a ser la nueva raiz de este
        subarbol, y el nodo original baja como su hijo izquierdo.

        Args:
            nodo (Nodo): Nodo desbalanceado sobre el cual rotar.

        Returns:
            Nodo: Nueva raiz del subarbol tras la rotacion.
        """
        pivote = nodo.derecha
        subarbol_temporal = pivote.izquierda

        pivote.izquierda = nodo
        nodo.derecha = subarbol_temporal

        self._actualizar_altura(nodo)
        self._actualizar_altura(pivote)

        return pivote

    def _balancear(self, nodo):
        """Balancea un nodo aplicando la rotacion AVL correspondiente.

        Evalua el factor de balance del nodo y, si esta fuera del
        rango permitido (-1 a 1), aplica la rotacion simple o doble
        que corresponda segun el caso (izquierda-izquierda,
        izquierda-derecha, derecha-derecha o derecha-izquierda).

        Args:
            nodo (Nodo): Nodo a evaluar y balancear.

        Returns:
            Nodo: Raiz del subarbol ya balanceado (puede ser el
            mismo nodo si no hizo falta rotar).
        """
        self._actualizar_altura(nodo)
        factor = self.factor_balance(nodo)

        if factor > 1:
            if self.factor_balance(nodo.izquierda) < 0:
                nodo.izquierda = self.rotacion_izquierda(nodo.izquierda)
            return self.rotacion_derecha(nodo)

        if factor < -1:
            if self.factor_balance(nodo.derecha) > 0:
                nodo.derecha = self.rotacion_derecha(nodo.derecha)
            return self.rotacion_izquierda(nodo)

        return nodo

    # --- Operaciones principales ---

    def insertar(self, valor):
        """Inserta un valor en el arbol, manteniendo el balance AVL.

        Args:
            valor: Valor a insertar.
        """
        self._raiz = self._insertar_recursivo(self._raiz, valor)

    def _insertar_recursivo(self, nodo, valor):
        """Inserta un valor de forma recursiva y balancea el camino.

        Args:
            nodo (Nodo | None): Nodo actual del recorrido.
            valor: Valor a insertar.

        Returns:
            Nodo: Raiz del subarbol (ya balanceada) tras la insercion.
        """
        if nodo is None:
            return Nodo(valor)

        if valor < nodo.valor:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, valor)
        else:
            return nodo  # Valor duplicado: no se inserta de nuevo.

        return self._balancear(nodo)

    def eliminar(self, valor):
        pass

    def _eliminar_recursivo(self, nodo, valor):
        pass

    def buscar(self, valor):
        """Busca un valor dentro del arbol.

        Args:
            valor: Valor a buscar.

        Returns:
            bool: True si el valor existe en el arbol, False si no.
        """
        return self._buscar_recursivo(self._raiz, valor) is not None

    def _buscar_recursivo(self, nodo, valor):
        """Busca un valor de forma recursiva.

        Args:
            nodo (Nodo | None): Nodo actual del recorrido.
            valor: Valor a buscar.

        Returns:
            Nodo | None: Nodo que contiene el valor, o None si no
            se encuentra.
        """
        if nodo is None or nodo.valor == valor:
            return nodo

        if valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierda, valor)
        return self._buscar_recursivo(nodo.derecha, valor)

    # --- Consultas ---

    def esta_vacio(self):
        """Indica si el arbol no tiene ningun nodo.

        Returns:
            bool: True si el arbol esta vacio, False en caso contrario.
        """
        return self._raiz is None

    @property
    def raiz(self):
        """Nodo raiz del arbol.

        Returns:
            Nodo | None: Nodo raiz, o None si el arbol esta vacio.
        """
        return self._raiz

    _SIN_ESPECIFICAR = object()

    def contar_nodos(self, nodo=_SIN_ESPECIFICAR):
        """Cuenta la cantidad total de nodos del arbol.

        Args:
            nodo (Nodo, optional): Nodo desde el cual contar. Si no
                se especifica, comienza desde la raiz.

        Returns:
            int: Cantidad de nodos en el subarbol.
        """
        if nodo is self._SIN_ESPECIFICAR:
            nodo = self._raiz
        if nodo is None:
            return 0
        return 1 + self.contar_nodos(nodo.izquierda) + self.contar_nodos(nodo.derecha)

    def __len__(self):
        """Permite usar len(arbol) para obtener la cantidad de nodos.

        Returns:
            int: Cantidad de nodos en el arbol.
        """
        return self.contar_nodos()

    def __str__(self):
        """Permite usar print(arbol) para ver su representacion.

        Returns:
            str: Arbol representado en texto mediante mostrar_arbol.
        """
        return self.mostrar_arbol()

    def minimo(self, nodo):
        """Encuentra el nodo con el menor valor de un subarbol.

        En un ABB, el minimo siempre esta en el extremo mas a la
        izquierda del subarbol.

        Args:
            nodo (Nodo): Nodo raiz del subarbol a evaluar.

        Returns:
            Nodo: Nodo con el valor minimo del subarbol.
        """
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual

    def maximo(self, nodo):
        """Encuentra el nodo con el mayor valor de un subarbol.

        En un ABB, el maximo siempre esta en el extremo mas a la
        derecha del subarbol.

        Args:
            nodo (Nodo): Nodo raiz del subarbol a evaluar.

        Returns:
            Nodo: Nodo con el valor maximo del subarbol.
        """
        actual = nodo
        while actual.derecha is not None:
            actual = actual.derecha
        return actual

    # --- Recorridos ---

    def preorden(self, nodo=_SIN_ESPECIFICAR, resultado=None):
        """Recorre el arbol en preorden (raiz, izquierda, derecha).

        Args:
            nodo (Nodo, optional): Nodo desde el cual continuar. Si
                no se especifica, comienza desde la raiz.
            resultado (list, optional): Lista acumuladora de valores.

        Returns:
            list: Valores del arbol en orden preorden.
        """
        if nodo is self._SIN_ESPECIFICAR:
            nodo = self._raiz
        if resultado is None:
            resultado = []
        if nodo is not None:
            resultado.append(nodo.valor)
            self.preorden(nodo.izquierda, resultado)
            self.preorden(nodo.derecha, resultado)
        return resultado

    def inorden(self, nodo=_SIN_ESPECIFICAR, resultado=None):
        """Recorre el arbol en inorden (izquierda, raiz, derecha).

        En un arbol de busqueda valido, este recorrido devuelve los
        valores ordenados de menor a mayor.

        Args:
            nodo (Nodo, optional): Nodo desde el cual continuar. Si
                no se especifica, comienza desde la raiz.
            resultado (list, optional): Lista acumuladora de valores.

        Returns:
            list: Valores del arbol en orden ascendente.
        """
        if nodo is self._SIN_ESPECIFICAR:
            nodo = self._raiz
        if resultado is None:
            resultado = []
        if nodo is not None:
            self.inorden(nodo.izquierda, resultado)
            resultado.append(nodo.valor)
            self.inorden(nodo.derecha, resultado)
        return resultado

    def postorden(self, nodo=_SIN_ESPECIFICAR, resultado=None):
        """Recorre el arbol en postorden (izquierda, derecha, raiz).

        Args:
            nodo (Nodo, optional): Nodo desde el cual continuar. Si
                no se especifica, comienza desde la raiz.
            resultado (list, optional): Lista acumuladora de valores.

        Returns:
            list: Valores del arbol en orden postorden.
        """
        if nodo is self._SIN_ESPECIFICAR:
            nodo = self._raiz
        if resultado is None:
            resultado = []
        if nodo is not None:
            self.postorden(nodo.izquierda, resultado)
            self.postorden(nodo.derecha, resultado)
            resultado.append(nodo.valor)
        return resultado

    def por_niveles(self):
        """Recorre el arbol nivel por nivel (BFS), de arriba a abajo.

        Returns:
            list: Valores del arbol ordenados por nivel de profundidad.
        """
        if self.esta_vacio():
            return []

        resultado = []
        cola = deque([self._raiz])

        while cola:
            nodo = cola.popleft()
            resultado.append(nodo.valor)
            if nodo.izquierda is not None:
                cola.append(nodo.izquierda)
            if nodo.derecha is not None:
                cola.append(nodo.derecha)

        return resultado

    # --- Visualizacion ---

    def mostrar_arbol(self, nodo=_SIN_ESPECIFICAR, prefijo='', es_ultimo=True,
                        es_raiz=True):
        """Genera una representacion en texto del arbol con conectores.

        Dibuja el arbol usando conectores de tipo '├──', '└──' y '│'
        (estilo comando 'tree'), lo cual permite visualizar su
        estructura de forma clara sin importar si es simetrico.

        Args:
            nodo (Nodo, optional): Nodo desde el cual continuar. Si
                no se especifica, comienza desde la raiz.
            prefijo (str, optional): Prefijo acumulado de espacios y
                lineas verticales heredado de los niveles anteriores.
            es_ultimo (bool, optional): Indica si el nodo actual es
                el ultimo hijo de su nodo padre.
            es_raiz (bool, optional): Indica si el nodo actual es la
                raiz del arbol completo.

        Returns:
            str: Texto con el arbol representado mediante conectores.
        """
        if nodo is self._SIN_ESPECIFICAR:
            nodo = self._raiz

        if nodo is None:
            return '' if not es_raiz else '(arbol vacio)'

        if es_raiz:
            texto = str(nodo.valor) + '\n'
            nuevo_prefijo = ''
        else:
            conector = '└── ' if es_ultimo else '├── '
            texto = prefijo + conector + str(nodo.valor) + '\n'
            nuevo_prefijo = prefijo + ('    ' if es_ultimo else '│   ')

        hijos = [h for h in (nodo.izquierda, nodo.derecha) if h is not None]
        for i, hijo in enumerate(hijos):
            ultimo = (i == len(hijos) - 1)
            texto += self.mostrar_arbol(hijo, nuevo_prefijo, ultimo, False)

        return texto


if __name__ == "__main__":
    pass