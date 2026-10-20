"""Compara el agente Minimax con el arbol de decision.

Mide tres cosas: la velocidad de cada agente, que tan precisas son
sus jugadas y como les va jugando partidas. Muestra los resultados en
pantalla y los guarda en data/resultados_comparacion.txt.
"""

import random
import statistics
import time
from collections import Counter

import pandas as pd

from model.game_model import GameModel
from model.minimax_agent import MinimaxAgent
from model.ml_agent import MLAgent, RUTA_DATASET

PARTIDAS = 1000
SEMILLA = 0
RUTA_RESULTADOS = RUTA_DATASET.parent / "resultados_comparacion.txt"


def tableros_posibles():
    """Lista los tableros con turno de O que pueden darse en una partida.

    Recorre todas las partidas legales posibles (X mueve primero) y
    junta cada tablero en el que le toca jugar a O.

    Returns:
        list[tuple]: Tableros como tuplas de 9 casillas, sin repetir.
    """
    vistos = set()
    modelo = GameModel()

    def recorrer():
        if modelo.is_game_over():
            return
        if modelo.current_player == 'O':
            vistos.add(tuple(modelo.board))
        for movimiento in modelo.get_available_moves():
            modelo.make_move(movimiento)
            modelo.switch_player()
            recorrer()
            modelo.undo_move(movimiento)
            modelo.switch_player()

    recorrer()
    return sorted(vistos)


def preparar(modelo, tablero):
    """Deja el modelo con un tablero dado y el turno de O.

    Args:
        modelo (GameModel): Modelo a modificar.
        tablero (tuple): Tablero de 9 casillas a cargar.
    """
    modelo.board = list(tablero)
    modelo.current_player = 'O'


def porcentaje(parte, total):
    """Calcula un porcentaje, devolviendo 0 si no hay elementos.

    Args:
        parte (int): Cantidad que se quiere expresar como porcentaje.
        total (int): Cantidad total.

    Returns:
        float: Porcentaje de parte sobre total.
    """
    return parte / total * 100 if total else 0.0


def jugadas_optimas(agente, modelo):
    """Obtiene las jugadas que Minimax puntua como las mejores.

    Puede haber mas de una jugada con el mejor puntaje.

    Args:
        agente (MinimaxAgent): Agente cuyo punto de vista se usa.
        modelo (GameModel): Modelo con el tablero a evaluar.

    Returns:
        set[int]: Casillas con el mejor puntaje posible.
    """
    puntajes = {}
    for movimiento in modelo.get_available_moves():
        modelo.make_move(movimiento, agente.ai_player)
        puntajes[movimiento] = agente.minimax(modelo, 0, False)
        modelo.undo_move(movimiento)
    mejor = max(puntajes.values())
    return {m for m, puntaje in puntajes.items() if puntaje == mejor}


def medir(agente, tableros, modelo):
    """Mide la jugada y el tiempo del agente en cada tablero.

    Args:
        agente (MinimaxAgent | MLAgent): Agente a medir.
        tableros (list[tuple]): Tableros donde juega el agente.
        modelo (GameModel): Modelo que se reutiliza para cada tablero.

    Returns:
        dict: Para cada tablero, la tupla (jugada, milisegundos,
        nodos explorados). Los nodos son None si el agente no explora.
    """
    resultados = {}
    for tablero in tableros:
        preparar(modelo, tablero)
        inicio = time.perf_counter()
        movimiento = agente.best_move(modelo)
        milisegundos = (time.perf_counter() - inicio) * 1000
        nodos = None
        if isinstance(agente, MinimaxAgent):
            nodos = agente.nodes_evaluated
        resultados[tablero] = (movimiento, milisegundos, nodos)
    return resultados


def seccion_velocidad(mm, ml):
    """Arma la seccion de velocidad del reporte.

    Args:
        mm (dict): Mediciones de Minimax, segun medir().
        ml (dict): Mediciones del arbol de decision, segun medir().

    Returns:
        list[str]: Lineas de texto de la seccion.
    """
    t_mm = [r[1] for r in mm.values()]
    t_ml = [r[1] for r in ml.values()]
    nodos = [r[2] for r in mm.values()]

    lineas = [
        f"1. VELOCIDAD (tiempo por jugada, {len(mm)} tableros posibles)",
        f"{'':<26}{'Minimax':>12}{'Arbol ML':>12}",
        f"{'Promedio (ms)':<26}"
        f"{statistics.mean(t_mm):>12.2f}{statistics.mean(t_ml):>12.2f}",
        f"{'Mediana (ms)':<26}"
        f"{statistics.median(t_mm):>12.2f}{statistics.median(t_ml):>12.2f}",
        f"{'Maximo (ms)':<26}{max(t_mm):>12.2f}{max(t_ml):>12.2f}",
        f"{'Nodos explorados (prom.)':<26}"
        f"{statistics.mean(nodos):>12.0f}{'-':>12}",
        "",
        "Por momento de la partida (promedios):",
        f"{'Jugada de O':<14}{'Tableros':>10}{'Minimax ms':>13}"
        f"{'Arbol ms':>11}{'Nodos Minimax':>16}",
    ]
    for ocupadas, nombre in ((1, '1ra'), (3, '2da'), (5, '3ra'), (7, '4ta')):
        grupo = [t for t in mm if 9 - t.count(' ') == ocupadas]
        lineas.append(
            f"{nombre:<14}{len(grupo):>10}"
            f"{statistics.mean(mm[t][1] for t in grupo):>13.2f}"
            f"{statistics.mean(ml[t][1] for t in grupo):>11.2f}"
            f"{statistics.mean(mm[t][2] for t in grupo):>16.0f}"
        )
    return lineas


def seccion_precision(mm, ml, optimas, grupos, ilegales):
    """Arma la seccion de precision de las jugadas del reporte.

    Args:
        mm (dict): Mediciones de Minimax, segun medir().
        ml (dict): Mediciones del arbol de decision, segun medir().
        optimas (dict): Jugadas optimas de cada tablero.
        grupos (dict): Nombre del grupo y lista de tableros.
        ilegales (float): Porcentaje de predicciones del arbol sobre
            una casilla ocupada, en los tableros que no vio.

    Returns:
        list[str]: Lineas de texto de la seccion.
    """
    lineas = [
        "2. PRECISION DE LAS JUGADAS DEL ARBOL (la jugada que realmente "
        "juega)",
        f"{'':<34}{'Tableros':>10}{'Igual a Minimax':>18}"
        f"{'Jugada optima':>16}",
    ]
    for nombre, grupo in grupos.items():
        iguales = sum(ml[t][0] == mm[t][0] for t in grupo)
        buenas = sum(ml[t][0] in optimas[t] for t in grupo)
        lineas.append(
            f"{nombre:<34}{len(grupo):>10}"
            f"{porcentaje(iguales, len(grupo)):>17.0f}%"
            f"{porcentaje(buenas, len(grupo)):>15.0f}%"
        )
    lineas += [
        "",
        "Minimax elige siempre una jugada optima (100%) por definicion.",
        "La cifra que mide si el arbol generaliza es la de los tableros "
        "que no vio.",
        f"Predicciones del arbol sobre casilla ocupada (tableros no "
        f"vistos): {ilegales:.0f}%",
        "En ese caso el agente juega la primera casilla libre.",
    ]
    return lineas


def con_cache(agente):
    """Envuelve a un agente para no recalcular jugadas repetidas.

    Minimax y el arbol siempre eligen lo mismo ante el mismo tablero,
    asi que alcanza con calcular cada jugada una vez.

    Args:
        agente (MinimaxAgent | MLAgent): Agente que juega como O.

    Returns:
        callable: Funcion que recibe el modelo y devuelve la jugada.
    """
    cache = {}

    def jugada(modelo):
        tablero = tuple(modelo.board)
        if tablero not in cache:
            cache[tablero] = agente.best_move(modelo)
        return cache[tablero]

    return jugada


def rival_aleatorio(rng):
    """Crea un rival X que elige siempre una casilla libre al azar.

    Args:
        rng (random.Random): Generador de numeros aleatorios.

    Returns:
        callable: Funcion que recibe el modelo y devuelve la jugada.
    """
    return lambda modelo: rng.choice(modelo.get_available_moves())


def rival_perfecto(rng):
    """Crea un rival X que juega perfecto, con desempate al azar.

    Es un Minimax que, entre sus jugadas optimas, elige una al azar.
    Nunca pierde, pero sus partidas varian.

    Args:
        rng (random.Random): Generador de numeros aleatorios.

    Returns:
        callable: Funcion que recibe el modelo y devuelve la jugada.
    """
    agente = MinimaxAgent(ai_player='X', human_player='O')
    cache = {}

    def jugada(modelo):
        tablero = tuple(modelo.board)
        if tablero not in cache:
            cache[tablero] = sorted(jugadas_optimas(agente, modelo))
        return rng.choice(cache[tablero])

    return jugada


def jugar_partidas(jugada_o, jugada_x):
    """Juega varias partidas entre un agente (O) y un rival (X).

    Args:
        jugada_o (callable): Funcion que elige la jugada de O.
        jugada_x (callable): Funcion que elige la jugada de X.

    Returns:
        Counter: Cantidad de partidas que gana, empata o pierde O.
    """
    resultados = Counter()
    for _ in range(PARTIDAS):
        modelo = GameModel()
        while not modelo.is_game_over():
            jugada = jugada_x if modelo.current_player == 'X' else jugada_o
            modelo.make_move(jugada(modelo))
            modelo.switch_player()

        if modelo.check_winner('O'):
            resultados['gana'] += 1
        elif modelo.check_winner('X'):
            resultados['pierde'] += 1
        else:
            resultados['empata'] += 1
    return resultados


def seccion_partidas(minimax, agente_ml):
    """Arma la seccion de resultados en partidas del reporte.

    Args:
        minimax (MinimaxAgent): Agente Minimax que juega como O.
        agente_ml (MLAgent): Agente de ML ya entrenado, juega como O.

    Returns:
        list[str]: Lineas de texto de la seccion.
    """
    rng = random.Random(SEMILLA)
    lineas = [
        f"3. PARTIDAS ({PARTIDAS} por enfrentamiento, el agente juega "
        "como O)",
        f"{'Rival (X)':<22}{'Agente':<12}{'Gana':>8}{'Empata':>9}"
        f"{'Pierde':>9}",
    ]
    rivales = (("Aleatorio", rival_aleatorio(rng)),
               ("Perfecto", rival_perfecto(rng)))
    agentes = (("Minimax", con_cache(minimax)),
               ("Arbol ML", con_cache(agente_ml)))

    for nombre_rival, jugada_x in rivales:
        for nombre_agente, jugada_o in agentes:
            r = jugar_partidas(jugada_o, jugada_x)
            lineas.append(
                f"{nombre_rival:<22}{nombre_agente:<12}{r['gana']:>8}"
                f"{r['empata']:>9}{r['pierde']:>9}"
            )
    lineas += [
        "",
        "Rival perfecto: Minimax que elige al azar entre sus jugadas "
        "optimas.",
    ]
    return lineas


def main():
    """Ejecuta la comparacion, la muestra y la guarda en un archivo."""
    modelo = GameModel()
    minimax = MinimaxAgent(ai_player='O', human_player='X')
    agente_ml = MLAgent(ai_player='O', human_player='X')
    tabla = agente_ml.cargar_csv()
    agente_ml.entrenar(tabla)

    tableros = tableros_posibles()
    preparar(modelo, tableros[0])
    agente_ml.best_move(modelo)  # Calentamiento, para no medir la carga.

    print("Midiendo velocidad (puede tardar un par de minutos)...")
    mm = medir(minimax, tableros, modelo)
    ml = medir(agente_ml, tableros, modelo)

    print("Calculando las jugadas optimas de cada tablero...")
    optimas = {}
    for tablero in tableros:
        preparar(modelo, tablero)
        optimas[tablero] = jugadas_optimas(minimax, modelo)

    entrenados = {tuple(f) for f in tabla[agente_ml.COLUMNAS].to_numpy()
                  .tolist()}
    vistos = [t for t in tableros
              if tuple(agente_ml.CODIFICACION[c] for c in t) in entrenados]
    no_vistos = [t for t in tableros if t not in set(vistos)]
    grupos = {
        "Todos los tableros": tableros,
        "Tableros que el arbol no vio": no_vistos,
        "Tableros de entrenamiento": vistos,
    }

    filas = [[agente_ml.CODIFICACION[c] for c in t] for t in tableros]
    crudas = agente_ml.clasificador.predict(
        pd.DataFrame(filas, columns=agente_ml.COLUMNAS)
    )
    prediccion = dict(zip(tableros, crudas))
    ilegales = porcentaje(
        sum(t[prediccion[t]] != ' ' for t in no_vistos), len(no_vistos)
    )

    print("Simulando partidas...")
    lineas = ["COMPARACION: MINIMAX VS ARBOL DE DECISION", ""]
    lineas += seccion_velocidad(mm, ml) + [""]
    lineas += seccion_precision(mm, ml, optimas, grupos, ilegales) + [""]
    lineas += seccion_partidas(minimax, agente_ml)

    texto = "\n".join(lineas)
    RUTA_RESULTADOS.write_text(texto + "\n", encoding="utf-8")
    print()
    print(texto)
    print()
    print(f"Resultados guardados en: {RUTA_RESULTADOS}")


if __name__ == "__main__":
    main()