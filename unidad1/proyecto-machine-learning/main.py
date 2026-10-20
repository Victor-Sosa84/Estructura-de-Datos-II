"""
titulo: Tres en Raya - MVC (Humano vs Humano, Humano vs IA (Minimax) 
y Humano vs IA (ML))
nombre: Victor David Sosa Coca
fecha: 20/10/2026
version: 3.0
"""

import tkinter as tk

from model.game_model import GameModel
from model.minimax_agent import MinimaxAgent
from model.ml_agent import MLAgent, RUTA_DATASET
from view.gui_view import GuiView
from controller.game_controller import GameController


def main():
    """Inicializa el modelo, los agentes, la vista y el controlador."""
    root = tk.Tk()

    modelo = GameModel()
    agente = MinimaxAgent(ai_player='O', human_player='X')

    agente_ml = MLAgent(ai_player='O', human_player='X')
    if not RUTA_DATASET.exists():
        agente_ml.generar_csv()
    agente_ml.entrenar()

    modos = [
        GameController.MODO_HUMANO,
        GameController.MODO_IA,
        GameController.MODO_ML,
    ]
    vista = GuiView(root, modos)
    GameController(modelo, vista, agente, agente_ml)

    root.mainloop()


if __name__ == "__main__":
    main()