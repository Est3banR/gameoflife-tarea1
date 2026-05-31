import numpy as np


class GameOfLife:
    def __init__(self, filas: int, columnas: int, estado_inicial=None) -> None:
        if filas <= 0 or columnas <= 0:
            raise ValueError("Las filas y columnas deben ser mayores que cero")

        self.filas = filas
        self.columnas = columnas

        if estado_inicial is None:
            self.tablero = np.random.randint(0, 2, size=(filas, columnas), dtype=np.uint8)
        else:
            tablero = np.array(estado_inicial, dtype=np.uint8)
            if tablero.shape != (filas, columnas):
                raise ValueError("El estado inicial no tiene el tamano correcto")
            # Cualquier valor mayor que cero se toma como celula viva.
            self.tablero = (tablero > 0).astype(np.uint8)

    def contar_vecinos(self) -> np.ndarray:
        # Determina cuantos vecinos vivos hay en la celula
        vecinos = np.zeros_like(self.tablero)

        # Se suman las 8 direcciones alrededor de cada celula.
        for fila in (-1, 0, 1):
            for columna in (-1, 0, 1):
                if fila == 0 and columna == 0: # (0,0) es la celula del centro
                    continue
                vecinos += np.roll(np.roll(self.tablero, fila, axis=0), columna, axis=1)
        return vecinos

    def step(self) -> None:
        # Cada paso es el avance de cada generacion de celulas
        vecinos = self.contar_vecinos()

        sobrevive = (self.tablero == 1) & ((vecinos == 2) | (vecinos == 3))
        nace = (self.tablero == 0) & (vecinos == 3)
        self.tablero = (sobrevive | nace).astype(np.uint8)

    def run(self, pasos: int) -> None:
        # Ejecuta varias generaciones
        if pasos < 0:
            raise ValueError("Los pasos no pueden ser negativos")

        for _ in range(pasos):
            self.step()

    def get_state(self) -> np.ndarray:
        # Retorna una copia del tablero actual
        return self.tablero.copy()

# Patrones conocidos para evaluarlos en las simulaciones
    @staticmethod
    def glider() -> np.ndarray:
        # Retorna un patron glider (mini grupo de celulas vivas)
        tablero = np.zeros((10, 10), dtype=np.uint8)
        tablero[1, 2] = 1
        tablero[2, 3] = 1
        tablero[3, 1:4] = 1
        return tablero

    @staticmethod
    def blinker() -> np.ndarray:
        # Retorna el patron blinker (mini grupo de celulas vivas)
        tablero = np.zeros((5, 5), dtype=np.uint8)
        tablero[2, 1:4] = 1
        return tablero

    @staticmethod
    def toad() -> np.ndarray:
        # Retorna el patron toad (mini grupo de celulas vivas)
        tablero = np.zeros((6, 6), dtype=np.uint8)
        tablero[2, 2:5] = 1
        tablero[3, 1:4] = 1
        return tablero
