"""Controlador del juego de Tres en Raya (Humano vs Humano y vs IA)."""


class GameController:
    """Orquesta la interaccion entre la vista, el modelo y la IA.

    Conecta los botones de la vista con la logica del juego, y en el
    modo Humano vs IA hace que el agente Minimax responda despues de
    cada jugada del humano. El humano juega siempre como 'X' y la IA
    como 'O'.

    Attributes:
        modelo (GameModel): Modelo que contiene el estado del juego.
        vista (GuiView): Vista sobre la cual se escuchan eventos y
            se muestran actualizaciones.
        agente (MinimaxAgent): Agente que juega como 'O' en el modo
            Humano vs IA.
        modo (str): Modo de la partida en curso.
    """

    MODO_HUMANO = "Humano vs Humano"
    MODO_IA = "Humano vs IA"

    def __init__(self, modelo, vista, agente):
        """Inicializa el controlador y conecta los botones de la vista.

        Args:
            modelo (GameModel): Instancia del modelo del juego.
            vista (GuiView): Instancia de la vista ya construida.
            agente (MinimaxAgent): Agente de IA que juega como 'O'.
        """
        self.modelo = modelo
        self.vista = vista
        self.agente = agente
        self.modo = self.MODO_HUMANO

        for posicion, boton in enumerate(self.vista.botones):
            boton["command"] = lambda pos=posicion: self.manejar_click(pos)

        self.vista.boton_empezar["command"] = self.iniciar_partida
        self.vista.boton_reiniciar["command"] = self.reiniciar_partida
        self.vista.boton_menu["command"] = self.volver_al_menu

    def manejar_click(self, posicion):
        """Maneja el click del humano sobre una casilla del tablero.

        Aplica la jugada del humano y, si la partida sigue y el modo
        es Humano vs IA, hace que la IA responda de inmediato.

        Args:
            posicion (int): Indice de la casilla clickeada (0-8).
        """
        if self.modelo.is_game_over():
            return

        if not self.modelo.is_valid_move(posicion):
            return  # Casilla ya ocupada, no hace nada.

        partida_terminada = self._jugar(posicion)

        if not partida_terminada and self.modo == self.MODO_IA:
            self._jugar(self.agente.best_move(self.modelo))

    def _jugar(self, posicion):
        """Aplica la jugada del jugador en turno y actualiza la vista.

        Args:
            posicion (int): Indice de la casilla (0-8) donde se juega.

        Returns:
            bool: True si la partida termino con esta jugada
            (victoria o empate), False si continua.
        """
        jugador = self.modelo.current_player
        self.modelo.make_move(posicion)
        self.vista.actualizar_casilla(posicion, jugador)

        if self.modelo.check_winner(jugador):
            self.vista.actualizar_estado(f"¡Gano {jugador}!")
            self.vista.mostrar_mensaje("Fin del juego", f"¡Gano {jugador}!")
            return True

        if self.modelo.is_draw():
            self.vista.actualizar_estado("¡Empate!")
            self.vista.mostrar_mensaje("Fin del juego", "¡Empate!")
            return True

        self.modelo.switch_player()
        self.vista.actualizar_estado(f"Turno: {self.modelo.current_player}")
        return False

    def iniciar_partida(self):
        """Empieza una partida en el modo elegido en el menu."""
        self.modo = self.vista.obtener_modo()
        self.reiniciar_partida()
        self.vista.mostrar_juego(self.modo)

    def reiniciar_partida(self):
        """Reinicia el modelo y la vista, manteniendo el mismo modo."""
        self.modelo.reset()
        self.vista.limpiar_tablero()
        self.vista.actualizar_estado(f"Turno: {self.modelo.current_player}")

    def volver_al_menu(self):
        """Vuelve al menu para poder elegir otro modo de juego."""
        self.vista.mostrar_menu()