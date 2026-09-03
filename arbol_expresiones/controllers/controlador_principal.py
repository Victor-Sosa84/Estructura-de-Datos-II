"""Controlador principal de la aplicacion.

Conecta la vista con el modelo: escucha el evento del boton,
valida la entrada, construye el arbol de expresion y actualiza
la vista con el resultado correspondiente (prefija o postfija).
"""

from models.arbol_expresion import ArbolExpresion


class ControladorPrincipal:
    """Orquesta la interaccion entre la vista y el modelo.

    Attributes:
        vista (VistaPrincipal): Vista sobre la cual se escuchan
            eventos y se muestran resultados.
    """

    def __init__(self, vista):
        """Inicializa el controlador y conecta el evento del boton.

        Args:
            vista (VistaPrincipal): Instancia de la vista principal
                ya construida.
        """
        self.vista = vista
        self.vista.boton_convertir.on_click = self.convertir

    def convertir(self, e):
        """Maneja el evento de clic en el boton Convertir.

        Valida que la expresion no este vacia, construye el arbol
        y muestra la prefija o postfija segun la opcion elegida.

        Args:
            e (ft.ControlEvent): Evento de clic emitido por Flet.
        """
        expresion = self.vista.campo_expresion.value

        if not expresion or not expresion.strip():
            self.vista.mostrar_error("Ingrese una expresion infija")
            return

        arbol = ArbolExpresion(expresion)
        modo = self.vista.opcion_conversion.value

        if modo == "prefija":
            resultado = arbol.obtener_prefija()
        else:
            resultado = arbol.obtener_postfija()

        self.vista.mostrar_resultado(resultado)