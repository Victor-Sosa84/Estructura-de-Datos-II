"""Agente de Machine Learning y generacion de su dataset."""

import random
from pathlib import Path

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import pandas as pd
from sklearn.model_selection import KFold, cross_val_score
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree

from model.game_model import GameModel
from model.minimax_agent import MinimaxAgent

RUTA_DATASET = Path(__file__).resolve().parent.parent / "data" / "dataset.csv"


class MLAgent:
    """Agente que aprende a jugar imitando a Minimax.

    Reune el pipeline de Machine Learning del proyecto. Por ahora
    implementa la preparacion de datos (simula partidas automaticas
    entre Minimax y un jugador aleatorio, registra cada decision de
    Minimax y la guarda como un dataset numerico en un CSV) y el
    entrenamiento de un arbol de decision que imita esas jugadas.

    Attributes:
        CODIFICACION (dict): Valor numerico de cada casilla, ya que
            el modelo solo trabaja con numeros: 'X' vale 1, 'O' vale
            -1 y vacia vale 0.
        COLUMNAS (list[str]): Nombres de las 9 columnas de entrada,
            una por casilla del tablero.
        COLUMNA_OBJETIVO (str): Nombre de la columna con la jugada
            que debe aprender a predecir el modelo.
        ai_player (str): Simbolo de la IA, que en las simulaciones
            juega como Minimax ('O').
        human_player (str): Simbolo del rival aleatorio, que mueve
            primero ('X'), igual que el humano en la aplicacion.
        clasificador (DecisionTreeClassifier | None): Arbol de
            decision entrenado, o None si todavia no se entreno.
    """

    CODIFICACION = {' ': 0, 'X': 1, 'O': -1}
    COLUMNAS = [f"casilla_{i}" for i in range(9)]
    COLUMNA_OBJETIVO = "jugada"

    def __init__(self, ai_player='O', human_player='X'):
        """Inicializa el agente indicando que simbolo juega cada lado.

        Args:
            ai_player (str, optional): Simbolo de la IA. Por defecto
                'O'.
            human_player (str, optional): Simbolo del rival aleatorio.
                Por defecto 'X'. Debe ser el que mueve primero en
                GameModel.
        """
        self.ai_player = ai_player
        self.human_player = human_player
        self.clasificador = None

    def simular_partida(self, minimax, rng, cache):
        """Simula una partida completa y registra las jugadas de la IA.

        El rival aleatorio mueve primero. Cada vez que le toca a la
        IA, su jugada la decide Minimax y se registra junto con el
        tablero en el que fue tomada.

        Args:
            minimax (MinimaxAgent): Agente que decide las jugadas de
                la IA.
            rng (random.Random): Generador que elige las jugadas del
                rival aleatorio.
            cache (dict): Jugadas de Minimax ya calculadas, por
                tablero. Minimax es determinista, asi que un tablero
                repetido no necesita recalcularse.

        Returns:
            list[tuple]: Registros (tablero, jugada), donde tablero es
            una tupla de 9 casillas (' ', 'X' u 'O') y jugada es el
            indice (0-8) que eligio Minimax.
        """
        modelo = GameModel()
        registros = []

        while not modelo.is_game_over():
            if modelo.current_player == self.human_player:
                movimiento = rng.choice(modelo.get_available_moves())
            else:
                tablero = tuple(modelo.board)
                if tablero not in cache:
                    cache[tablero] = minimax.best_move(modelo)
                movimiento = cache[tablero]
                registros.append((tablero, movimiento))

            modelo.make_move(movimiento)
            modelo.switch_player()

        return registros

    def generar_dataset(self, partidas=1000, semilla=None):
        """Genera el dataset simulando partidas automaticas.

        Args:
            partidas (int, optional): Cantidad de partidas a simular.
                Por defecto 1000.
            semilla (int, optional): Semilla del generador aleatorio,
                para obtener siempre el mismo dataset. Si es None, el
                resultado cambia en cada ejecucion.

        Returns:
            list[tuple]: Registros (tablero, jugada) de todas las
            partidas simuladas, en el formato de simular_partida.
        """
        minimax = MinimaxAgent(self.ai_player, self.human_player)
        rng = random.Random(semilla)
        cache = {}
        dataset = []

        for _ in range(partidas):
            dataset.extend(self.simular_partida(minimax, rng, cache))

        return dataset

    def a_dataframe(self, dataset):
        """Convierte los registros en una tabla numerica sin repetidos.

        Cada tablero pasa a 9 columnas de entrada (casillas
        codificadas) mas la columna de la jugada. Se deja un solo
        registro por tablero: Minimax siempre elige lo mismo ante el
        mismo tablero, asi que los repetidos no aportan informacion
        y, al separar entrenamiento y prueba, harian que el mismo
        tablero apareciera en ambos lados.

        Args:
            dataset (list[tuple]): Registros (tablero, jugada) tal
                como los devuelve generar_dataset.

        Returns:
            pd.DataFrame: Tabla con una fila por tablero distinto.
        """
        filas = [
            [self.CODIFICACION[casilla] for casilla in tablero] + [jugada]
            for tablero, jugada in dataset
        ]
        tabla = pd.DataFrame(
            filas, columns=self.COLUMNAS + [self.COLUMNA_OBJETIVO]
        )
        tabla = tabla.drop_duplicates(subset=self.COLUMNAS)
        return tabla.reset_index(drop=True)

    def guardar_csv(self, tabla, ruta=RUTA_DATASET):
        """Guarda la tabla en un archivo CSV, creando la carpeta.

        Args:
            tabla (pd.DataFrame): Tabla a guardar.
            ruta (str | Path, optional): Destino del archivo. Por
                defecto data/dataset.csv dentro del proyecto.
        """
        ruta = Path(ruta)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        tabla.to_csv(ruta, index=False)

    def cargar_csv(self, ruta=RUTA_DATASET):
        """Lee el dataset desde un archivo CSV.

        Args:
            ruta (str | Path, optional): Archivo a leer. Por defecto
                data/dataset.csv dentro del proyecto.

        Returns:
            pd.DataFrame: Tabla con las columnas de entrada y la
            jugada.
        """
        return pd.read_csv(ruta)

    def generar_csv(self, partidas=1000, semilla=42, ruta=RUTA_DATASET):
        """Simula las partidas y deja el dataset listo en un CSV.

        Args:
            partidas (int, optional): Cantidad de partidas a
                simular. Por defecto 1000.
            semilla (int, optional): Semilla del generador aleatorio,
                para obtener siempre el mismo dataset. Por defecto 42.
            ruta (str | Path, optional): Destino del archivo. Por
                defecto data/dataset.csv dentro del proyecto.

        Returns:
            pd.DataFrame: Tabla guardada en el CSV.
        """
        dataset = self.generar_dataset(partidas, semilla)
        tabla = self.a_dataframe(dataset)
        self.guardar_csv(tabla, ruta)
        return tabla

    def _crear_clasificador(self):
        """Crea un arbol de decision sin entrenar.

        Se usa tanto para entrenar como para medir la precision, asi
        ambos trabajan con la misma configuracion.

        Returns:
            DecisionTreeClassifier: Arbol nuevo, con semilla fija para
            que el resultado sea siempre el mismo.
        """
        return DecisionTreeClassifier(random_state=0)

    def _requerir_entrenado(self):
        """Verifica que el arbol de decision ya este entrenado.

        Raises:
            RuntimeError: Si todavia no se llamo a entrenar().
        """
        if self.clasificador is None:
            raise RuntimeError("El modelo no esta entrenado: llamar a "
                               "entrenar() primero.")

    def entrenar(self, tabla=None):
        """Entrena el arbol de decision con el dataset.

        El arbol aprende a predecir la jugada de Minimax (columna
        objetivo) a partir de las 9 casillas del tablero.

        Args:
            tabla (pd.DataFrame, optional): Dataset de entrenamiento.
                Si no se especifica, se lee desde el CSV.
        """
        if tabla is None:
            tabla = self.cargar_csv()

        self.clasificador = self._crear_clasificador()
        self.clasificador.fit(
            tabla[self.COLUMNAS], tabla[self.COLUMNA_OBJETIVO]
        )

    def evaluar_precision(self, tabla=None, repartos=5, semilla=0):
        """Mide con que frecuencia el arbol coincide con Minimax.

        Usa validacion cruzada: reparte los tableros en varios grupos
        y, por turnos, entrena con todos menos uno y prueba con el que
        quedo afuera. Asi la precision se mide siempre sobre tableros
        que el arbol no vio, y el resultado no depende de un unico
        reparto afortunado o desafortunado.

        Args:
            tabla (pd.DataFrame, optional): Dataset a evaluar. Si no
                se especifica, se lee desde el CSV.
            repartos (int, optional): Cantidad de grupos. Por
                defecto 5.
            semilla (int, optional): Semilla del reparto aleatorio.

        Returns:
            tuple[float, float, float]: Precision promedio, minima y
            maxima entre los repartos, en porcentaje.
        """
        if tabla is None:
            tabla = self.cargar_csv()

        puntajes = cross_val_score(
            self._crear_clasificador(),
            tabla[self.COLUMNAS],
            tabla[self.COLUMNA_OBJETIVO],
            cv=KFold(n_splits=repartos, shuffle=True, random_state=semilla),
        )
        return (puntajes.mean() * 100,
                puntajes.min() * 100,
                puntajes.max() * 100)

    def exportar_reglas(self, max_depth=None):
        """Describe en texto las reglas que aprendio el arbol.

        En las reglas, cada casilla vale 1 si tiene 'X', -1 si tiene
        'O' y 0 si esta vacia.

        Args:
            max_depth (int, optional): Profundidad maxima a mostrar.
                Si no se especifica, se muestra el arbol completo.

        Returns:
            str: Reglas del arbol, una por linea, con sangria.
        """
        self._requerir_entrenado()
        profundidad = max_depth or self.clasificador.get_depth()
        return export_text(
            self.clasificador,
            feature_names=self.COLUMNAS,
            max_depth=profundidad,
        )

    def dibujar_arbol(self, ruta, max_depth=3):
        """Guarda un grafico del arbol de decision como imagen.

        Un arbol completo tiene cientos de nodos y no se puede leer en
        una imagen, por eso por defecto solo se dibujan los primeros
        niveles. Para ver todas las reglas esta exportar_reglas.

        Args:
            ruta (str | Path): Archivo de imagen de destino (PNG).
            max_depth (int, optional): Niveles a dibujar. Por
                defecto 3.
        """
        self._requerir_entrenado()
        figura = Figure(figsize=(34, 10))
        FigureCanvasAgg(figura)  # Lienzo en memoria: sin abrir ventanas.
        ejes = figura.subplots()
        plot_tree(
            self.clasificador,
            feature_names=self.COLUMNAS,
            class_names=[f"casilla {c}" for c in self.clasificador.classes_],
            max_depth=max_depth,
            filled=True,
            fontsize=9,
            ax=ejes,
        )
        figura.savefig(ruta, dpi=150, bbox_inches="tight")

    def best_move(self, modelo):
        """Elige la jugada de la IA segun lo que aprendio el arbol.

        El arbol predice la casilla que habria elegido Minimax. Como
        puede equivocarse y proponer una casilla ya ocupada, en ese
        caso se juega la primera casilla libre. Asume que la IA juega
        como 'O', igual que en los datos de entrenamiento.

        Args:
            modelo (GameModel): Modelo del juego con el tablero actual.

        Returns:
            int | None: Indice de la casilla elegida (0-8), o None si
            no hay casillas libres.
        """
        self._requerir_entrenado()
        disponibles = modelo.get_available_moves()
        if not disponibles:
            return None

        casillas = [self.CODIFICACION[c] for c in modelo.board]
        fila = pd.DataFrame([casillas], columns=self.COLUMNAS)
        prediccion = int(self.clasificador.predict(fila)[0])

        return prediccion if prediccion in disponibles else disponibles[0]
