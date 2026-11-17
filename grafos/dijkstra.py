
import heapq


def dijkstra(grafo, inicio, destino):
    """Encuentra el camino más corto entre dos vértices."""
    distancias = {
        vertice: float("inf")
        for vertice in grafo
    }

    anteriores = {
        vertice: None
        for vertice in grafo
    }

    distancias[inicio] = 0
    cola = [(0, inicio)]

    while cola:
        distancia_actual, actual = heapq.heappop(cola)

        if distancia_actual > distancias[actual]:
            continue

        if actual == destino:
            break

        for vecino, peso in grafo[actual]:
            nueva_distancia = distancia_actual + peso

            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                anteriores[vecino] = actual

                heapq.heappush(
                    cola,
                    (nueva_distancia, vecino)
                )

    # Comprobar si existe un camino al destino.
    if distancias[destino] == float("inf"):
        return float("inf"), []

    # Reconstruir el camino desde el destino.
    camino = []
    actual = destino

    while actual is not None:
        camino.append(actual)
        actual = anteriores[actual]

    camino.reverse()

    return distancias[destino], camino


def main():
    """Ejecuta un ejemplo del algoritmo de Dijkstra."""
    grafo = {
        "A": [("B", 4), ("C", 2)],
        "B": [("A", 4), ("C", 1), ("D", 5), ("E", 7)],
        "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
        "D": [("B", 5), ("C", 8), ("E", 2)],
        "E": [("B", 7), ("C", 10), ("D", 2)]
    }

    inicio = "A"
    destino = "D"

    costo, camino = dijkstra(
        grafo,
        inicio,
        destino
    )

    if camino:
        print(f"Camino más corto: {' -> '.join(camino)}")
        print(f"Costo del camino: {costo}")
    else:
        print("No existe un camino entre los vértices.")


if __name__ == "__main__":
    main()
