"""Modelo del juego de Tres en Raya."""


class GameModel:
    """Modelo del juego de Tres en Raya.

    Mantiene el estado del tablero y las reglas del juego: validacion
    de movimientos, deteccion de victoria y de empate. No contiene
    nada relacionado a interfaz grafica.

    Attributes:
        board (list): Lista de 9 posiciones (0-8) representando el
            tablero 3x3. Cada posicion vale ' ' (vacia), 'X' u 'O'.
        current_player (str): Jugador al que le toca mover ('X' u 'O').
    """

    COMBINACIONES_GANADORAS = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # filas
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columnas
        (0, 4, 8), (2, 4, 6),             # diagonales
    ]

    def __init__(self):
        """Inicializa un tablero vacio con 'X' como primer jugador."""
        self.board = [' '] * 9
        self.current_player = 'X'

    def get_available_moves(self):
        """Obtiene las posiciones vacias del tablero.

        Returns:
            list[int]: Indices (0-8) de las casillas disponibles.
        """
        return [i for i, casilla in enumerate(self.board) if casilla == ' ']

    def is_valid_move(self, posicion):
        """Verifica si una posicion es un movimiento valido.

        Args:
            posicion (int): Indice de la casilla (0-8).

        Returns:
            bool: True si la posicion esta dentro del tablero y vacia.
        """
        return 0 <= posicion <= 8 and self.board[posicion] == ' '

    def make_move(self, posicion, jugador=None):
        """Coloca la ficha de un jugador en una posicion del tablero.

        Args:
            posicion (int): Indice de la casilla (0-8).
            jugador (str, optional): Jugador que realiza el movimiento
                ('X' u 'O'). Si no se especifica, usa el jugador
                actual del turno.

        Returns:
            bool: True si el movimiento se realizo, False si la
            posicion no era valida.
        """
        if not self.is_valid_move(posicion):
            return False

        self.board[posicion] = jugador if jugador else self.current_player
        return True

    def undo_move(self, posicion):
        """Deshace un movimiento, dejando la casilla vacia de nuevo.

        Args:
            posicion (int): Indice de la casilla (0-8) a vaciar.
        """
        self.board[posicion] = ' '

    def check_winner(self, jugador):
        """Verifica si un jugador especifico ha ganado la partida.

        Args:
            jugador (str): Jugador a verificar ('X' u 'O').

        Returns:
            bool: True si el jugador tiene una combinacion ganadora.
        """
        for a, b, c in self.COMBINACIONES_GANADORAS:
            if self.board[a] == self.board[b] == self.board[c] == jugador:
                return True
        return False

    def is_draw(self):
        """Verifica si la partida termino en empate.

        Returns:
            bool: True si el tablero esta lleno y nadie gano.
        """
        tablero_lleno = len(self.get_available_moves()) == 0
        alguien_gano = self.check_winner('X') or self.check_winner('O')
        return tablero_lleno and not alguien_gano

    def is_game_over(self):
        """Verifica si la partida ya termino (victoria o empate).

        Returns:
            bool: True si hay un ganador o la partida esta empatada.
        """
        return self.check_winner('X') or self.check_winner('O') or self.is_draw()

    def switch_player(self):
        """Cambia el turno al otro jugador."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def reset(self):
        """Reinicia el tablero a su estado inicial."""
        self.board = [' '] * 9
        self.current_player = 'X'