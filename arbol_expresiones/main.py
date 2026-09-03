"""Punto de entrada de la aplicacion.

Inicializa la aplicacion Flet, construye la vista principal y la
conecta con su controlador.
"""

import flet as ft

from views.vista_principal import VistaPrincipal
from controllers.controlador_principal import ControladorPrincipal


def main(page: ft.Page):
    """Configura la pagina y arranca la vista con su controlador.

    Args:
        page (ft.Page): Pagina principal provista por Flet.
    """
    vista = VistaPrincipal(page)
    ControladorPrincipal(vista)


if __name__ == "__main__":
    ft.app(target=main)