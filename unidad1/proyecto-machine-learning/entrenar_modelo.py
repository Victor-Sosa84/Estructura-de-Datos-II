"""Entrena el arbol de decision y exporta sus reglas y su grafico."""

from model.ml_agent import MLAgent, RUTA_DATASET

CARPETA_SALIDA = RUTA_DATASET.parent


def main():
    """Entrena el modelo, mide su precision y guarda sus resultados."""
    agente = MLAgent()
    tabla = agente.cargar_csv()
    agente.entrenar(tabla)

    media, minima, maxima = agente.evaluar_precision(tabla)
    print(f"Tableros de entrenamiento: {len(tabla)}")
    print(f"Profundidad del arbol: {agente.clasificador.get_depth()}")
    print(f"Hojas del arbol: {agente.clasificador.get_n_leaves()}")
    print(f"Precision (validacion cruzada): {media:.0f}% promedio, "
          f"entre {minima:.0f}% y {maxima:.0f}%")

    ruta_reglas = CARPETA_SALIDA / "reglas_arbol.txt"
    ruta_imagen = CARPETA_SALIDA / "arbol_decision.png"
    ruta_reglas.write_text(agente.exportar_reglas(), encoding="utf-8")
    agente.dibujar_arbol(ruta_imagen)

    print(f"Reglas guardadas en: {ruta_reglas}")
    print(f"Grafico guardado en: {ruta_imagen}")


if __name__ == "__main__":
    main()
