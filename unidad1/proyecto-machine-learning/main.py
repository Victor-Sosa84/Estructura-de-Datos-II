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


def centrar_ventana(root):
    """Centra la ventana en la pantalla segun su tamaño actual.

    Args:
        root (tk.Tk): Ventana a centrar.
    """
    root.update_idletasks()
    ancho = root.winfo_width()
    alto = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (ancho // 2)
    y = (root.winfo_screenheight() // 2) - (alto // 2)
    root.geometry(f"{ancho}x{alto}+{x}+{y}")


def main():
    """Inicializa el modelo, la vista y el controlador del juego."""
    root = tk.Tk()

    modelo = GameModel()
    vista = GuiView(root)
    GameController(modelo, vista)

    centrar_ventana(root)

    root.mainloop()


if __name__ == "__main__":
    main()