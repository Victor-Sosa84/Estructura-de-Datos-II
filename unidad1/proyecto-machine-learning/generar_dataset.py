"""Genera el dataset de entrenamiento del agente de ML (se corre una vez)."""

from model.ml_agent import MLAgent, RUTA_DATASET


def main():
    """Simula las partidas y guarda el dataset en data/dataset.csv."""
    agente = MLAgent()
    tabla = agente.generar_csv()
    print(f"Dataset guardado en: {RUTA_DATASET}")
    print(f"Filas (tableros distintos): {len(tabla)}")


if __name__ == "__main__":
    main()