
from collections import deque


class Grafo:
    """Representa un grafo no dirigido mediante listas de adyacencia."""

    def __init__(self):
        self.adyacencias = {}

    def agregar_vertice(self, vertice):
        """Agrega un vértice al grafo."""
        if vertice not in self.adyacencias:
            self.adyacencias[vertice] = []

    def agregar_arista(self, origen, destino):
        """Agrega una arista entre dos vértices."""
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)

        if destino not in self.adyacencias[origen]:
            self.adyacencias[origen].append(destino)

        if origen not in self.adyacencias[destino]:
            self.adyacencias[destino].append(origen)

    def mostrar(self):
        """Muestra las listas de adyacencia del grafo."""
        for vertice, vecinos in self.adyacencias.items():
            print(f"{vertice}: {vecinos}")

    def bfs(self, inicio):
        """Realiza un recorrido en anchura usando una cola."""
        if inicio not in self.adyacencias:
            raise ValueError("El vértice inicial no existe.")

        visitados = {inicio}
        cola = deque([inicio])
        recorrido = []

        while cola:
            actual = cola.popleft()
            recorrido.append(actual)

            for vecino in self.adyacencias[actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)

        return recorrido

    def dfs(self, inicio):
        """Realiza un recorrido en profundidad usando recursividad."""
        if inicio not in self.adyacencias:
            raise ValueError("El vértice inicial no existe.")

        visitados = set()
        recorrido = []

        def visitar(vertice):
            visitados.add(vertice)
            recorrido.append(vertice)

            for vecino in self.adyacencias[vertice]:
                if vecino not in visitados:
                    visitar(vecino)

        visitar(inicio)

        return recorrido


def main():
    """Crea un grafo y ejecuta los recorridos BFS y DFS."""
    grafo = Grafo()

    # Agregar vértices.
    for vertice in ["A", "B", "C", "D", "E"]:
        grafo.agregar_vertice(vertice)

    # Agregar aristas.
    grafo.agregar_arista("A", "B")
    grafo.agregar_arista("A", "C")
    grafo.agregar_arista("B", "D")
    grafo.agregar_arista("C", "D")
    grafo.agregar_arista("C", "E")

    # Mostrar el grafo.
    print("Grafo:")
    grafo.mostrar()

    # Recorridos desde el vértice A.
    print("\nBFS:", " -> ".join(grafo.bfs("A")))
    print("DFS:", " -> ".join(grafo.dfs("A")))


if __name__ == "__main__":
    main()
