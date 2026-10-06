"""Vista grafica del juego de Tres en Raya, implementada en Tkinter."""

import tkinter as tk


class GuiView:
    """Interfaz grafica del tablero de Tres en Raya.

    Construye un tablero 3x3 de botones y expone referencias a ellos
    para que el controlador pueda leerlos y actualizarlos. No
    contiene logica de juego: solo arma la interfaz.

    Attributes:
        root (tk.Tk): Ventana principal de la aplicacion.
        botones (list[tk.Button]): Lista de 9 botones, uno por
            casilla del tablero (indices 0-8).
        etiqueta_estado (tk.Label): Texto que muestra el turno
            actual o el resultado de la partida.
    """

    def __init__(self, root):
        """Inicializa y construye la interfaz sobre la ventana dada.

        Args:
            root (tk.Tk): Ventana principal donde se arma la interfaz.
        """
        self.root = root
        self.root.title("Tres en Raya")

        self.etiqueta_estado = tk.Label(root, text="Turno: X", font=("Arial", 14))
        self.etiqueta_estado.grid(row=0, column=0, columnspan=3, pady=10)

        self.botones = []
        for posicion in range(9):
            boton = tk.Button(root, text=" ", font=("Arial", 24), width=4, height=2)
            fila = 1 + posicion // 3
            columna = posicion % 3
            boton.grid(row=fila, column=columna)
            self.botones.append(boton)

        self.boton_reiniciar = tk.Button(root, text="Reiniciar")
        self.boton_reiniciar.grid(row=4, column=0, columnspan=3, pady=10)

    def actualizar_casilla(self, posicion, valor):
        """Actualiza el texto mostrado en una casilla del tablero.

        Args:
            posicion (int): Indice de la casilla (0-8) a actualizar.
            valor (str): Texto a mostrar ('X', 'O' o ' ').
        """
        self.botones[posicion]["text"] = valor

    def actualizar_estado(self, mensaje):
        """Actualiza el mensaje de estado (turno o resultado).

        Args:
            mensaje (str): Texto a mostrar en la etiqueta de estado.
        """
        self.etiqueta_estado["text"] = mensaje

    def limpiar_tablero(self):
        """Vacia visualmente las 9 casillas del tablero."""
        for boton in self.botones:
            boton["text"] = " "