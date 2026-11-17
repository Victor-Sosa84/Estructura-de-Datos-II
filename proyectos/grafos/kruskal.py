
def kruskal(vertices, aristas):
    """Encuentra el árbol de expansión mínima de un grafo."""
    padres = {vertice: vertice for vertice in vertices}
    rangos = {vertice: 0 for vertice in vertices}

    def buscar(vertice):
        """Encuentra la raíz del conjunto de un vértice."""
        if padres[vertice] != vertice:
            padres[vertice] = buscar(padres[vertice])

        return padres[vertice]

    def unir(vertice_a, vertice_b):
        """Une dos conjuntos si no forman un ciclo."""
        raiz_a = buscar(vertice_a)
        raiz_b = buscar(vertice_b)

        if raiz_a == raiz_b:
            return False

        if rangos[raiz_a] < rangos[raiz_b]:
            padres[raiz_a] = raiz_b
        elif rangos[raiz_a] > rangos[raiz_b]:
            padres[raiz_b] = raiz_a
        else:
            padres[raiz_b] = raiz_a
            rangos[raiz_a] += 1

        return True

    arbol_minimo = []
    costo_total = 0

    # Ordenar las aristas por peso, de menor a mayor.
    aristas_ordenadas = sorted(
        aristas,
        key=lambda arista: arista[2]
    )

    for vertice_a, vertice_b, peso in aristas_ordenadas:
        if unir(vertice_a, vertice_b):
            arbol_minimo.append(
                (vertice_a, vertice_b, peso)
            )
            costo_total += peso

        if len(arbol_minimo) == len(vertices) - 1:
            break

    if len(arbol_minimo) != len(vertices) - 1:
        raise ValueError("El grafo no es conexo.")

    return arbol_minimo, costo_total


def main():
    """Ejecuta un ejemplo del algoritmo de Kruskal."""
    vertices = ["A", "B", "C", "D", "E"]

    aristas = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 1),
        ("B", "D", 5),
        ("C", "D", 8),
        ("C", "E", 10),
        ("D", "E", 2),
        ("B", "E", 7)
    ]

    arbol_minimo, costo_total = kruskal(
        vertices,
        aristas
    )

    print("Aristas seleccionadas:")

    for vertice_a, vertice_b, peso in arbol_minimo:
        print(f"{vertice_a} - {vertice_b}: {peso}")

    print(f"Costo mínimo total: {costo_total}")


if __name__ == "__main__":
    main()
