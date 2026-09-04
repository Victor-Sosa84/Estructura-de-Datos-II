"""Vista principal de la aplicacion.

Construye los controles visuales (entrada, seleccion de modo,
boton y salida) usando Flet. No contiene logica de negocio: solo
arma la interfaz y expone referencias a sus controles para que el
controlador pueda leerlos y actualizarlos.
"""

import flet as ft


class VistaPrincipal:
    """Interfaz grafica para el conversor de expresiones.

    Attributes:
        page (ft.Page): Pagina de Flet sobre la que se construye
            la interfaz.
        campo_expresion (ft.TextField): Campo de entrada para la
            expresion infija.
        opcion_conversion (ft.RadioGroup): Selector entre
            conversion a prefija o postfija.
        boton_convertir (ft.ElevatedButton): Boton que dispara la
            conversion.
        campo_resultado (ft.TextField): Campo de solo lectura donde
            se muestra el resultado.
    """

    def __init__(self, page):
        """Inicializa y construye la interfaz sobre la pagina dada.

        Args:
            page (ft.Page): Pagina de Flet donde se agregan los
                controles.
        """
        self.page = page
        self.page.title = "Conversor de Expresiones"

        self.campo_expresion = ft.TextField(
            label="Expresion infija",
            hint_text="Ej: a+b*c",
        )

        self.opcion_conversion = ft.RadioGroup(
            value="prefija",
            content=ft.Row(
                controls=[
                    ft.Radio(value="prefija", label="Prefija"),
                    ft.Radio(value="postfija", label="Postfija"),
                ]
            ),
        )

        self.boton_convertir = ft.ElevatedButton(text="Convertir")

        self.campo_resultado = ft.TextField(
            label="Resultado",
            read_only=True,
        )

        self.page.add(
            self.campo_expresion,
            self.opcion_conversion,
            self.boton_convertir,
            self.campo_resultado,
        )

    def mostrar_resultado(self, texto):
        """Muestra un texto en el campo de resultado.

        Args:
            texto (str): Texto a mostrar como resultado.
        """
        self.campo_resultado.value = texto
        self.page.update()

    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error mediante un snackbar.

        Args:
            mensaje (str): Mensaje de error a mostrar.
        """
        self.page.open(ft.SnackBar(content=ft.Text(mensaje)))