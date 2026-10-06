"""
titulo: Proyecto Machine Learning - Tres en Raya - MVC
nombre: Victor David Sosa Coca
fecha: 06/10/2026
version: 1.0
"""

import tkinter as tk

from model.game_model import GameModel
from view.gui_view import GuiView
from controller.game_controller import GameController


def main():
    """Inicializa el modelo, la vista y el controlador del juego."""
    root = tk.Tk()

    modelo = GameModel()
    vista = GuiView(root)
    GameController(modelo, vista)

    root.mainloop()


if __name__ == "__main__":
    main()