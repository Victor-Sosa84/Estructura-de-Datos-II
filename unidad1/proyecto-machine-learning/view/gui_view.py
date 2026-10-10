"""Vista grafica del juego de Tres en Raya, implementada en Tkinter."""

import tkinter as tk
from tkinter import messagebox, ttk


class GuiView:
    """Interfaz grafica del tablero de Tres en Raya.

    Maneja dos pantallas dentro de la misma ventana: un menu donde se
    elige el modo de juego, y la pantalla del tablero. Expone
    referencias a sus controles para que el controlador pueda leerlos
    y actualizarlos. No contiene logica de juego: solo arma la
    interfaz.

    Attributes:
        root (tk.Tk): Ventana principal de la aplicacion.
        modos (list[str]): Modos de juego disponibles en el menu.
        selector_modo (ttk.Combobox): Desplegable para elegir el modo.
        boton_empezar (tk.Button): Boton que inicia la partida.
        etiqueta_modo (tk.Label): Titulo con el modo de la partida
            en curso.
        etiqueta_estado (tk.Label): Texto que muestra el turno
            actual o el resultado de la partida.
        botones (list[tk.Button]): Lista de 9 botones, uno por
            casilla del tablero (indices 0-8).
        boton_reiniciar (tk.Button): Reinicia la partida en el
            mismo modo.
        boton_menu (tk.Button): Vuelve al menu de seleccion de modo.
    """

    def __init__(self, root, modos=None):
        """Inicializa y construye las dos pantallas sobre la ventana.

        Args:
            root (tk.Tk): Ventana principal donde se arma la interfaz.
            modos (list[str], optional): Modos de juego a ofrecer en
                el menu. Por defecto Humano vs Humano y Humano vs IA.
        """
        self.root = root
        self.root.title("Tres en Raya")
        self.modos = modos if modos else ["Humano vs Humano", "Humano vs IA"]

        self._construir_menu()
        self._construir_juego()
        self.mostrar_menu()

    def _construir_menu(self):
        """Arma la pantalla de menu con el selector de modo."""
        self.frame_menu = tk.Frame(self.root, padx=40, pady=30)

        tk.Label(self.frame_menu, text="Tres en Raya", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.frame_menu, text="Modo de juego:").pack()

        self.selector_modo = ttk.Combobox(
            self.frame_menu, values=self.modos, state="readonly"
        )
        self.selector_modo.current(0)
        self.selector_modo.pack(pady=10)

        self.boton_empezar = tk.Button(self.frame_menu, text="Empezar")
        self.boton_empezar.pack(pady=10)

    def _construir_juego(self):
        """Arma la pantalla de juego con el tablero y sus botones."""
        self.frame_juego = tk.Frame(self.root, padx=10, pady=10)

        self.etiqueta_modo = tk.Label(
            self.frame_juego, text="", font=("Arial", 14, "bold")
        )
        self.etiqueta_modo.grid(row=0, column=0, columnspan=3, pady=(0, 5))

        self.etiqueta_estado = tk.Label(
            self.frame_juego, text="Turno: X", font=("Arial", 14)
        )
        self.etiqueta_estado.grid(row=1, column=0, columnspan=3, pady=5)

        self.botones = []
        for posicion in range(9):
            boton = tk.Button(
                self.frame_juego, text=" ", font=("Arial", 24), width=4, height=2
            )
            fila = 2 + posicion // 3
            columna = posicion % 3
            boton.grid(row=fila, column=columna)
            self.botones.append(boton)

        frame_acciones = tk.Frame(self.frame_juego)
        frame_acciones.grid(row=5, column=0, columnspan=3, pady=10)

        self.boton_reiniciar = tk.Button(frame_acciones, text="Reiniciar")
        self.boton_reiniciar.pack(side=tk.LEFT, padx=5)

        self.boton_menu = tk.Button(frame_acciones, text="Volver al menu")
        self.boton_menu.pack(side=tk.LEFT, padx=5)

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

    def mostrar_mensaje(self, titulo, mensaje):
        """Muestra un mensaje emergente al usuario.

        Args:
            titulo (str): Titulo de la ventana del mensaje.
            mensaje (str): Texto del mensaje.
        """
        messagebox.showinfo(titulo, mensaje)

    def obtener_modo(self):
        """Obtiene el modo de juego elegido en el menu.

        Returns:
            str: Texto del modo seleccionado en el desplegable.
        """
        return self.selector_modo.get()

    def mostrar_menu(self):
        """Muestra la pantalla de menu y oculta la del juego."""
        self.frame_juego.pack_forget()
        self.frame_menu.pack()
        self._centrar_ventana()

    def mostrar_juego(self, modo):
        """Muestra la pantalla del tablero y oculta el menu.

        Args:
            modo (str): Modo de la partida, mostrado como titulo.
        """
        self.frame_menu.pack_forget()
        self.etiqueta_modo["text"] = modo
        self.frame_juego.pack()
        self._centrar_ventana()

    def _centrar_ventana(self):
        """Ajusta la ventana al contenido actual y la centra."""
        self.root.geometry("")
        self.root.update_idletasks()
        ancho = self.root.winfo_reqwidth()
        alto = self.root.winfo_reqheight()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"+{x}+{y}")