"""
titulo: Proyecto Machine Learning - Tres en Raya - MVC (Humano vs Humano y Humano vs IA)
nombre: Victor David Sosa Coca
fecha: 13/10/2026
version: 2.0
"""


import tkinter as tk

from model.game_model import GameModel
from model.minimax_agent import MinimaxAgent
from view.gui_view import GuiView
from controller.game_controller import GameController


def main():
    """Inicializa el modelo, el agente, la vista y el controlador."""
    root = tk.Tk()

    modelo = GameModel()
    agente = MinimaxAgent(ai_player='O', human_player='X')
    vista = GuiView(root, [GameController.MODO_HUMANO, GameController.MODO_IA])
    GameController(modelo, vista, agente)

    root.mainloop()


if __name__ == "__main__":
    main()