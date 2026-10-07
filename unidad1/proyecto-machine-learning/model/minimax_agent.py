"""Agente de IA basado en el algoritmo Minimax con Backtracking."""


class MinimaxAgent:
    """Agente que decide jugadas optimas mediante el algoritmo Minimax.

    Explora de forma recursiva el arbol de jugadas futuras del juego,
    aplicando y deshaciendo movimientos sobre el tablero (tecnica de
    Backtracking) para simular cada posible partida sin necesidad de
    copiar el tablero en cada nivel de recursion.

    Attributes:
        ai_player (str): Simbolo que representa a la IA ('X' u 'O').
        human_player (str): Simbolo que representa al humano.
        nodes_evaluated (int): Cantidad de nodos (tableros) evaluados
            durante la ultima busqueda, con fines educativos.
    """

    def __init__(self, ai_player='O', human_player='X'):
        """Inicializa el agente indicando que simbolo juega cada lado.

        Args:
            ai_player (str, optional): Simbolo de la IA. Por defecto 'O'.
            human_player (str, optional): Simbolo del humano. Por
                defecto 'X'.
        """
        self.ai_player = ai_player
        self.human_player = human_player
        self.nodes_evaluated = 0

    def evaluate(self, modelo):
        """Evalua un tablero terminal segun el resultado de la partida.

        Esta es la funcion de evaluacion heuristica: solo tiene
        sentido llamarla sobre un tablero donde la partida ya termino
        (victoria o empate), ya que Minimax la usa en los nodos hoja
        del arbol de jugadas.

        Args:
            modelo (GameModel): Modelo del juego con el tablero actual.

        Returns:
            int: +10 si gana la IA, -10 si gana el humano, 0 en
            cualquier otro caso (empate).
        """
        if modelo.check_winner(self.ai_player):
            return 10
        if modelo.check_winner(self.human_player):
            return -10
        return 0

    def minimax(self, modelo, depth, is_maximizing):
        """Calcula el puntaje optimo de un tablero mediante Minimax.

        Recorre recursivamente el arbol de jugadas futuras alternando
        entre maximizar (turno de la IA) y minimizar (turno del
        humano). Aplica y deshace cada movimiento hipotetico sobre el
        mismo tablero (Backtracking), en vez de copiarlo en cada
        nivel de recursion.

        Args:
            modelo (GameModel): Modelo del juego con el tablero actual.
            depth (int): Profundidad actual de la recursion. Se usa
                para preferir victorias rapidas y retrasar derrotas.
            is_maximizing (bool): True si es el turno de la IA
                (maximiza el puntaje), False si es el turno del
                humano (minimiza el puntaje).

        Returns:
            int: Puntaje optimo alcanzable desde este tablero.
        """
        self.nodes_evaluated += 1

        if modelo.check_winner(self.ai_player):
            return 10 - depth
        if modelo.check_winner(self.human_player):
            return depth - 10
        if not modelo.get_available_moves():
            return 0

        jugador_actual = self.ai_player if is_maximizing else self.human_player

        if is_maximizing:
            mejor_puntaje = float('-inf')
            for movimiento in modelo.get_available_moves():
                modelo.make_move(movimiento, jugador_actual)
                puntaje = self.minimax(modelo, depth + 1, False)
                modelo.undo_move(movimiento)  # Backtracking.
                mejor_puntaje = max(puntaje, mejor_puntaje)
            return mejor_puntaje

        mejor_puntaje = float('inf')
        for movimiento in modelo.get_available_moves():
            modelo.make_move(movimiento, jugador_actual)
            puntaje = self.minimax(modelo, depth + 1, True)
            modelo.undo_move(movimiento)  # Backtracking.
            mejor_puntaje = min(puntaje, mejor_puntaje)
        return mejor_puntaje

    def best_move(self, modelo):
        """Determina la mejor jugada disponible para la IA.

        Prueba cada movimiento posible, calcula su puntaje mediante
        Minimax, y devuelve el que maximiza el resultado para la IA.

        Args:
            modelo (GameModel): Modelo del juego con el tablero actual.

        Returns:
            int | None: Indice de la mejor casilla (0-8), o None si
            no hay movimientos disponibles.
        """
        self.nodes_evaluated = 0
        mejor_puntaje = float('-inf')
        mejor_movimiento = None

        for movimiento in modelo.get_available_moves():
            modelo.make_move(movimiento, self.ai_player)
            puntaje = self.minimax(modelo, 0, False)
            modelo.undo_move(movimiento)  # Backtracking.

            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_movimiento = movimiento

        return mejor_movimiento