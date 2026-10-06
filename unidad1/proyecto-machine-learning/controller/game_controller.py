"""Controlador del juego de Tres en Raya, modo Humano vs Humano."""

from tkinter import messagebox


class GameController:
    """Orquesta la interaccion entre la vista y el modelo del juego.

    Conecta cada boton del tablero con la logica de movimiento del
    modelo, y actualiza la vista segun el resultado de cada jugada.

    Attributes:
        modelo (GameModel): Modelo que contiene el estado del juego.
        vista (GuiView): Vista sobre la cual se escuchan eventos y
            se muestran actualizaciones.
    """

    def __init__(self, modelo, vista):
        """Inicializa el controlador y conecta los botones del tablero.

        Args:
            modelo (GameModel): Instancia del modelo del juego.
            vista (GuiView): Instancia de la vista ya construida.
        """
        self.modelo = modelo
        self.vista = vista

        for posicion, boton in enumerate(self.vista.botones):
            boton["command"] = lambda pos=posicion: self.manejar_click(pos)

        self.vista.boton_reiniciar["command"] = self.reiniciar_partida

    def manejar_click(self, posicion):
        """Maneja el click sobre una casilla del tablero.

        Valida el movimiento, actualiza el modelo y la vista, y
        verifica si la partida termino (victoria o empate).

        Args:
            posicion (int): Indice de la casilla clickeada (0-8).
        """
        if self.modelo.is_game_over():
            return

        if not self.modelo.make_move(posicion):
            return  # Casilla ya ocupada, no hace nada.

        self.vista.actualizar_casilla(posicion, self.modelo.current_player)

        if self.modelo.check_winner(self.modelo.current_player):
            self.vista.actualizar_estado(f"¡Gano {self.modelo.current_player}!")
            messagebox.showinfo("Fin del juego", f"¡Gano {self.modelo.current_player}!")
            return

        if self.modelo.is_draw():
            self.vista.actualizar_estado("¡Empate!")
            messagebox.showinfo("Fin del juego", "¡Empate!")
            return

        self.modelo.switch_player()
        self.vista.actualizar_estado(f"Turno: {self.modelo.current_player}")

    def reiniciar_partida(self):
        """Reinicia el modelo y la vista para empezar una nueva partida."""
        self.modelo.reset()
        self.vista.limpiar_tablero()
        self.vista.actualizar_estado(f"Turno: {self.modelo.current_player}")