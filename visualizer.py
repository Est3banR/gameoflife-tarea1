from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

from game_of_life import GameOfLife


carpeta_salida = Path("outputs")


def centrar_patron(patron: np.ndarray, tamano: int) -> np.ndarray:
    # Coloca un patron pequeno en el centro de un tablero cuadrado
    if patron.shape[0] > tamano or patron.shape[1] > tamano:
        raise ValueError("El tamano del tablero debe ser mayor que el patron")

    tablero = np.zeros((tamano, tamano), dtype=np.uint8)
    fila = (tamano - patron.shape[0]) // 2
    columna = (tamano - patron.shape[1]) // 2
    tablero[fila : fila + patron.shape[0], columna : columna + patron.shape[1]] = patron
    return tablero


def crear_estado_inicial(nombre: str, tamano: int):
    # Crea un patron inicial segun el valor dentro del dicc
    patrones = {
        "glider": GameOfLife.glider(),
        "blinker": GameOfLife.blinker(),
        "toad": GameOfLife.toad(),
    }

    if nombre == "random":
        return None
    if nombre not in patrones:
        raise ValueError("Usa uno de estos patrones: random, glider, blinker, toad")

    return centrar_patron(patrones[nombre], tamano)


def animate_game(nombre: str, tamano: int, pasos: int) -> Path:
    # Hace un gif para mostrar la simulacion
    carpeta_salida.mkdir(exist_ok=True)

    estado_inicial = crear_estado_inicial(nombre, tamano)
    juego = GameOfLife(tamano, tamano, estado_inicial)
    ruta_gif = carpeta_salida / f"{nombre}_{tamano}.gif"

    figura, eje = plt.subplots(figsize=(6, 6))
    imagen = eje.imshow(juego.get_state(), cmap="binary", vmin=0, vmax=1)
    eje.set_title(f"{nombre.title()} - {tamano}x{tamano}")
    eje.set_xticks([])
    eje.set_yticks([])

    def actualizar(_frame):
        imagen.set_array(juego.get_state())
        juego.step()
        return (imagen,)

    animacion = FuncAnimation(figura, actualizar, frames=pasos, interval=100, blit=True)
    animacion.save(ruta_gif, writer=PillowWriter(fps=10))
    plt.close(figura)
    return ruta_gif


if __name__ == "__main__":
    animate_game("glider", 32, 50)
    animate_game("blinker", 32, 20)
    animate_game("random", 128, 100)
