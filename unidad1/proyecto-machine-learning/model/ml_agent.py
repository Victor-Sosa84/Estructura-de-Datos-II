"""Agente de Machine Learning y generacion de su dataset."""

import random

from model.game_model import GameModel
from model.minimax_agent import MinimaxAgent


class MLAgent:
    """Agente que aprende a jugar imitando a Minimax.

    Reune el pipeline de Machine Learning del proyecto. Por ahora
    implementa la generacion de datos: simula partidas automaticas
    entre Minimax y un jugador aleatorio, y registra cada decision
    de Minimax para usarla luego como ejemplo de entrenamiento.

    Attributes:
        ai_player (str): Simbolo de la IA, que en las simulaciones
            juega como Minimax ('O').
        human_player (str): Simbolo del rival aleatorio, que mueve
            primero ('X'), igual que el humano en la aplicacion.
    """

    def __init__(self, ai_player='O', human_player='X'):
        """Inicializa el agente indicando que simbolo juega cada lado.

        Args:
            ai_player (str, optional): Simbolo de la IA. Por defecto
                'O'.
            human_player (str, optional): Simbolo del rival aleatorio.
                Por defecto 'X'. Debe ser el que mueve primero en
                GameModel.
        """
        self.ai_player = ai_player
        self.human_player = human_player

    def simular_partida(self, minimax, rng, cache):
        """Simula una partida completa y registra las jugadas de la IA.

        El rival aleatorio mueve primero. Cada vez que le toca a la
        IA, su jugada la decide Minimax y se registra junto con el
        tablero en el que fue tomada.

        Args:
            minimax (MinimaxAgent): Agente que decide las jugadas de
                la IA.
            rng (random.Random): Generador que elige las jugadas del
                rival aleatorio.
            cache (dict): Jugadas de Minimax ya calculadas, por
                tablero. Minimax es determinista, asi que un tablero
                repetido no necesita recalcularse.

        Returns:
            list[tuple]: Registros (tablero, jugada), donde tablero es
            una tupla de 9 casillas (' ', 'X' u 'O') y jugada es el
            indice (0-8) que eligio Minimax.
        """
        modelo = GameModel()
        registros = []

        while not modelo.is_game_over():
            if modelo.current_player == self.human_player:
                movimiento = rng.choice(modelo.get_available_moves())
            else:
                tablero = tuple(modelo.board)
                if tablero not in cache:
                    cache[tablero] = minimax.best_move(modelo)
                movimiento = cache[tablero]
                registros.append((tablero, movimiento))

            modelo.make_move(movimiento)
            modelo.switch_player()

        return registros

    def generar_dataset(self, partidas=1000, semilla=None):
        """Genera el dataset simulando partidas automaticas.

        Args:
            partidas (int, optional): Cantidad de partidas a simular.
                Por defecto 1000.
            semilla (int, optional): Semilla del generador aleatorio,
                para obtener siempre el mismo dataset. Si es None, el
                resultado cambia en cada ejecucion.

        Returns:
            list[tuple]: Registros (tablero, jugada) de todas las
            partidas simuladas, en el formato de simular_partida.
        """
        minimax = MinimaxAgent(self.ai_player, self.human_player)
        rng = random.Random(semilla)
        cache = {}
        dataset = []

        for _ in range(partidas):
            dataset.extend(self.simular_partida(minimax, rng, cache))

        return dataset