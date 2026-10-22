"""Compara el agente Minimax con el arbol de decision.

Mide cuatro cosas: la velocidad de cada agente, que tan precisas son
sus jugadas, como les va jugando partidas y como es el modelo
entrenado. Muestra los resultados en pantalla, los guarda en
data/resultados_comparacion.txt y deja el detalle de cada tablero en
data/detalle_comparacion.csv.
"""

import random
import statistics
import time
import warnings
from collections import Counter

import numpy as np
import pandas as pd

from model.game_model import GameModel
from model.minimax_agent import MinimaxAgent
from model.ml_agent import MLAgent, RUTA_DATASET

PARTIDAS = 1000
SEMILLA = 0
REPETICIONES = 3
RUTA_RESULTADOS = RUTA_DATASET.parent / "resultados_comparacion.txt"
RUTA_DETALLE = RUTA_DATASET.parent / "detalle_comparacion.csv"


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


def signo(numero):
    """Devuelve 1, 0 o -1 segun el signo del numero.

    Args:
        numero (int): Numero a evaluar.

    Returns:
        int: 1 si es positivo, -1 si es negativo, 0 si es cero.
    """
    return (numero > 0) - (numero < 0)


def jugadas_buenas(agente, modelo):
    """Clasifica las jugadas de un tablero segun su puntaje Minimax.

    Minimax resta la profundidad al puntaje, asi que prefiere ganar
    rapido. Por eso se calculan dos conjuntos: las jugadas con el
    mejor puntaje exacto y las que, aunque tarden mas, no empeoran el
    resultado (ganar sigue siendo ganar, empatar sigue siendo empatar).

    Args:
        agente (MinimaxAgent): Agente cuyo punto de vista se usa.
        modelo (GameModel): Modelo con el tablero a evaluar.

    Returns:
        tuple[set[int], set[int]]: Casillas con el mejor puntaje y
        casillas que conservan el resultado teorico.
    """
    puntajes = {}
    for movimiento in modelo.get_available_moves():
        modelo.make_move(movimiento, agente.ai_player)
        puntajes[movimiento] = agente.minimax(modelo, 0, False)
        modelo.undo_move(movimiento)
    mejor = max(puntajes.values())
    optimas = {m for m, p in puntajes.items() if p == mejor}
    conservan = {m for m, p in puntajes.items()
                 if signo(p) == signo(mejor)}
    return optimas, conservan


def medir(agente, tableros, modelo):
    """Mide la jugada y el tiempo del agente en cada tablero.

    El tiempo es el mejor de REPETICIONES intentos, para reducir el
    ruido de otros procesos del sistema.

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
        tiempos = []
        for _ in range(REPETICIONES):
            inicio = time.perf_counter()
            movimiento = agente.best_move(modelo)
            tiempos.append((time.perf_counter() - inicio) * 1000)
        nodos = None
        if isinstance(agente, MinimaxAgent):
            nodos = agente.nodes_evaluated
        resultados[tablero] = (movimiento, min(tiempos), nodos)
    return resultados


def medir_prediccion(agente_ml, tableros):
    """Mide solo la prediccion del arbol, sin armar un DataFrame.

    best_move arma un DataFrame de pandas en cada jugada y sklearn
    valida la entrada, y eso cuesta mucho mas que recorrer el arbol.
    Aqui se usa un arreglo de numpy para aislar la inferencia.

    Args:
        agente_ml (MLAgent): Agente de ML ya entrenado.
        tableros (list[tuple]): Tableros donde se mide.

    Returns:
        list[float]: Milisegundos de cada prediccion.
    """
    clasificador = agente_ml.clasificador
    tiempos = []
    with warnings.catch_warnings():
        # El arbol se entreno con nombres de columna; numpy no los tiene.
        warnings.simplefilter("ignore")
        for tablero in tableros:
            fila = np.array([[agente_ml.CODIFICACION[c] for c in tablero]])
            mejor = float('inf')
            for _ in range(REPETICIONES):
                inicio = time.perf_counter()
                clasificador.predict(fila)
                mejor = min(mejor, (time.perf_counter() - inicio) * 1000)
            tiempos.append(mejor)
    return tiempos


def seccion_velocidad(mm, ml, t_pred):
    """Arma la seccion de velocidad del reporte.

    Args:
        mm (dict): Mediciones de Minimax, segun medir().
        ml (dict): Mediciones del arbol de decision, segun medir().
        t_pred (list[float]): Tiempos de la prediccion sola del arbol,
            segun medir_prediccion().

    Returns:
        list[str]: Lineas de texto de la seccion.
    """
    t_mm = [r[1] for r in mm.values()]
    t_ml = [r[1] for r in ml.values()]
    nodos = [r[2] for r in mm.values()]

    lineas = [
        f"1. VELOCIDAD (mejor de {REPETICIONES} intentos por jugada, "
        f"{len(mm)} tableros posibles)",
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
        if not grupo:
            continue
        lineas.append(
            f"{nombre:<14}{len(grupo):>10}"
            f"{statistics.mean(mm[t][1] for t in grupo):>13.2f}"
            f"{statistics.mean(ml[t][1] for t in grupo):>11.2f}"
            f"{statistics.mean(mm[t][2] for t in grupo):>16.0f}"
        )
    lineas += [
        "",
        "Del tiempo del arbol, casi todo es costo de pandas y sklearn "
        "al preparar la entrada.",
        f"Solo la prediccion (numpy, promedio): "
        f"{statistics.mean(t_pred):.3f} ms por jugada.",
    ]
    return lineas


def seccion_precision(mm, ml, buenas, grupos, ilegales):
    """Arma la seccion de precision de las jugadas del reporte.

    Args:
        mm (dict): Mediciones de Minimax, segun medir().
        ml (dict): Mediciones del arbol de decision, segun medir().
        buenas (dict): Para cada tablero, la tupla (jugadas optimas,
            jugadas que conservan el resultado), segun
            jugadas_buenas().
        grupos (dict): Nombre del grupo y lista de tableros.
        ilegales (float): Porcentaje de predicciones del arbol sobre
            una casilla ocupada, en los tableros que no vio.

    Returns:
        list[str]: Lineas de texto de la seccion.
    """
    lineas = [
        "2. PRECISION DE LAS JUGADAS DEL ARBOL (la jugada que realmente "
        "juega)",
        f"{'':<30}{'Tableros':>10}{'Igual a Minimax':>17}"
        f"{'Optima':>9}{'No empeora':>12}",
    ]
    for nombre, grupo in grupos.items():
        iguales = sum(ml[t][0] == mm[t][0] for t in grupo)
        optimas = sum(ml[t][0] in buenas[t][0] for t in grupo)
        conservan = sum(ml[t][0] in buenas[t][1] for t in grupo)
        lineas.append(
            f"{nombre:<30}{len(grupo):>10}"
            f"{porcentaje(iguales, len(grupo)):>16.0f}%"
            f"{porcentaje(optimas, len(grupo)):>8.0f}%"
            f"{porcentaje(conservan, len(grupo)):>11.0f}%"
        )
    lineas += [
        "",
        "Igual a Minimax: misma casilla que elige Minimax.",
        "Optima: casilla con el mejor puntaje (gana o empata lo mas "
        "rapido posible).",
        "No empeora: conserva el resultado teorico (gana, empata o "
        "pierde igual).",
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
            optimas, _ = jugadas_buenas(agente, modelo)
            cache[tablero] = sorted(optimas)
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

    Cada enfrentamiento arranca con un generador aleatorio nuevo y
    con la misma semilla, asi ambos agentes juegan contra rivales en
    las mismas condiciones.

    Args:
        minimax (MinimaxAgent): Agente Minimax que juega como O.
        agente_ml (MLAgent): Agente de ML ya entrenado, juega como O.

    Returns:
        list[str]: Lineas de texto de la seccion.
    """
    lineas = [
        f"3. PARTIDAS ({PARTIDAS} por enfrentamiento, el agente juega "
        "como O)",
        f"{'Rival (X)':<22}{'Agente':<12}{'Gana':>8}{'Empata':>9}"
        f"{'Pierde':>9}",
    ]
    rivales = (("Aleatorio", rival_aleatorio),
               ("Perfecto", rival_perfecto))
    agentes = (("Minimax", con_cache(minimax)),
               ("Arbol ML", con_cache(agente_ml)))
    derrotas_minimax = 0

    for nombre_rival, crear_rival in rivales:
        for nombre_agente, jugada_o in agentes:
            jugada_x = crear_rival(random.Random(SEMILLA))
            r = jugar_partidas(jugada_o, jugada_x)
            if nombre_agente == "Minimax":
                derrotas_minimax += r['pierde']
            lineas.append(
                f"{nombre_rival:<22}{nombre_agente:<12}{r['gana']:>8}"
                f"{r['empata']:>9}{r['pierde']:>9}"
            )
    invicto = "SI" if derrotas_minimax == 0 else "NO"
    lineas += [
        "",
        "Rival perfecto: Minimax que elige al azar entre sus jugadas "
        "optimas.",
        f"Minimax invicto (0 derrotas en total): {invicto}",
    ]
    return lineas


def seccion_modelo(agente_ml, tabla):
    """Arma la seccion con los datos del modelo entrenado.

    Args:
        agente_ml (MLAgent): Agente de ML ya entrenado.
        tabla (pd.DataFrame): Dataset con el que se entreno.

    Returns:
        list[str]: Lineas de texto de la seccion.
    """
    clasificador = agente_ml.clasificador
    promedio, minimo, maximo = agente_ml.evaluar_precision(tabla)
    return [
        "4. DATOS DEL MODELO",
        f"Tableros en el dataset: {len(tabla)}",
        f"Profundidad del arbol: {clasificador.get_depth()}",
        f"Hojas del arbol: {clasificador.get_n_leaves()}",
        "Validacion cruzada (misma casilla que Minimax, sobre tableros "
        "no vistos):",
        f"  promedio {promedio:.1f}%, minimo {minimo:.1f}%, "
        f"maximo {maximo:.1f}%",
    ]


def clasificar_tableros(agente_ml, tabla, tableros):
    """Separa los tableros que el arbol vio al entrenar de los que no.

    Args:
        agente_ml (MLAgent): Agente de ML, para la codificacion.
        tabla (pd.DataFrame): Dataset con el que se entreno.
        tableros (list[tuple]): Tableros a clasificar.

    Returns:
        tuple[list, list]: Tableros vistos y tableros no vistos.
    """
    filas = tabla[agente_ml.COLUMNAS].to_numpy().tolist()
    entrenados = {tuple(fila) for fila in filas}
    vistos, no_vistos = [], []
    for tablero in tableros:
        codigo = tuple(agente_ml.CODIFICACION[c] for c in tablero)
        if codigo in entrenados:
            vistos.append(tablero)
        else:
            no_vistos.append(tablero)
    return vistos, no_vistos


def porcentaje_ilegales(agente_ml, no_vistos):
    """Calcula cuantas predicciones del arbol caen en casilla ocupada.

    Args:
        agente_ml (MLAgent): Agente de ML ya entrenado.
        no_vistos (list[tuple]): Tableros que el arbol no vio.

    Returns:
        float: Porcentaje de predicciones sobre una casilla ocupada.
    """
    filas = [[agente_ml.CODIFICACION[c] for c in t] for t in no_vistos]
    predicciones = agente_ml.clasificador.predict(
        pd.DataFrame(filas, columns=agente_ml.COLUMNAS)
    )
    ocupadas = sum(t[p] != ' ' for t, p in zip(no_vistos, predicciones))
    return porcentaje(ocupadas, len(no_vistos))


def guardar_detalle(mm, ml, buenas, vistos):
    """Guarda en un CSV el resultado de cada tablero, para graficar.

    Args:
        mm (dict): Mediciones de Minimax, segun medir().
        ml (dict): Mediciones del arbol de decision, segun medir().
        buenas (dict): Jugadas optimas y que conservan el resultado
            de cada tablero, segun jugadas_buenas().
        vistos (list[tuple]): Tableros usados en el entrenamiento.
    """
    vistos = set(vistos)
    filas = [
        {
            "tablero": "".join(t).replace(' ', '_'),
            "visto_al_entrenar": t in vistos,
            "jugada_minimax": mm[t][0],
            "jugada_arbol": ml[t][0],
            "ms_minimax": mm[t][1],
            "ms_arbol": ml[t][1],
            "nodos_minimax": mm[t][2],
            "arbol_optima": ml[t][0] in buenas[t][0],
            "arbol_no_empeora": ml[t][0] in buenas[t][1],
        }
        for t in mm
    ]
    pd.DataFrame(filas).to_csv(RUTA_DETALLE, index=False)


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

    print("Midiendo velocidad...")
    mm = medir(minimax, tableros, modelo)
    ml = medir(agente_ml, tableros, modelo)
    t_pred = medir_prediccion(agente_ml, tableros)

    print("Calculando las jugadas buenas de cada tablero...")
    buenas = {}
    for tablero in tableros:
        preparar(modelo, tablero)
        buenas[tablero] = jugadas_buenas(minimax, modelo)

    vistos, no_vistos = clasificar_tableros(agente_ml, tabla, tableros)
    grupos = {
        "Todos los tableros": tableros,
        "Tableros que el arbol no vio": no_vistos,
        "Tableros de entrenamiento": vistos,
    }
    ilegales = porcentaje_ilegales(agente_ml, no_vistos)

    print("Simulando partidas...")
    lineas = ["COMPARACION: MINIMAX VS ARBOL DE DECISION", ""]
    lineas += seccion_velocidad(mm, ml, t_pred) + [""]
    lineas += seccion_precision(mm, ml, buenas, grupos, ilegales) + [""]
    lineas += seccion_partidas(minimax, agente_ml) + [""]
    lineas += seccion_modelo(agente_ml, tabla)

    texto = "\n".join(lineas)
    RUTA_RESULTADOS.write_text(texto + "\n", encoding="utf-8")
    guardar_detalle(mm, ml, buenas, vistos)
    print()
    print(texto)
    print()
    print(f"Resultados guardados en: {RUTA_RESULTADOS}")
    print(f"Detalle por tablero en: {RUTA_DETALLE}")


if __name__ == "__main__":
    main()
