import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from time import perf_counter
from game_of_life import GameOfLife

carpeta_salida = Path("outputs")
size = [32, 64, 128, 256, 512, 1024]
pasos = 10


def medir_tamano(tamano: int) -> float:
    # Retorna el tiempo promedio por generacion en ms
    juego = GameOfLife(tamano, tamano)
    inicio = perf_counter()
    juego.run(pasos)
    total = perf_counter() - inicio

    return (total / pasos) * 1000


def estimar_complejidad(celdas: np.ndarray, tiempos: np.ndarray) -> str:
    # Calcula si el tiempo del programa crece similar a 0(n)
    pendiente = np.polyfit(np.log(celdas), np.log(tiempos), 1)[0]

    if pendiente < 1.25:
        return f"O(n) aproximado, pendiente {pendiente:.2f}"
    if pendiente < 1.75:
        return f"entre O(n) y O(n^2), pendiente {pendiente:.2f}"
    return f"O(n^2) aproximado, pendiente {pendiente:.2f}"


def guardar_graficas(celdas: np.ndarray, tiempos: np.ndarray) -> None:
    # Retorna las graficas de rendimiento
    carpeta_salida.mkdir(exist_ok=True)

    # Las curvas teoricas se escalan para iniciar en el primer tiempo medido.
    curva_lineal = celdas / celdas[0] * tiempos[0]
    curva_cuadratica = (celdas / celdas[0]) ** 2 * tiempos[0]

    plt.figure(figsize=(9, 6))
    plt.plot(celdas, tiempos, "o-", label="Medido")
    plt.plot(celdas, curva_lineal, "--", label="O(n)")
    plt.plot(celdas, curva_cuadratica, "--", label="O(n^2)")
    plt.xlabel("Numero de celdas")
    plt.ylabel("ms por generacion")
    plt.title("Benchmark Lineal")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(carpeta_salida / "benchmark_linear.png", dpi=150)
    plt.close()

    plt.figure(figsize=(9, 6))
    plt.loglog(celdas, tiempos, "o-", label="Medido")
    plt.loglog(celdas, curva_lineal, "--", label="O(n)")
    plt.loglog(celdas, curva_cuadratica, "--", label="O(n^2)")
    plt.xlabel("Numero de celdas")
    plt.ylabel("ms por generacion")
    plt.title("Benchmark (log-log)")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(carpeta_salida / "benchmark_loglog.png", dpi=150)
    plt.close()


def main() -> None:
    resultados = []

    for tamano in size:
        tiempo = medir_tamano(tamano)
        resultados.append((tamano, tamano * tamano, tiempo))

    celdas = np.array([fila[1] for fila in resultados], dtype=float)
    tiempos = np.array([fila[2] for fila in resultados], dtype=float)
    complejidad = estimar_complejidad(celdas, tiempos)

    print(f"{'Tamano':>8} | {'Celdas':>10} | {'ms/generacion':>14}")
    print("-" * 40)
    for tamano, cantidad_celdas, tiempo in resultados:
        print(f"{tamano:>8} | {cantidad_celdas:>10} | {tiempo:>14.4f}")

    print(f"\nComplejidad estimada: {complejidad}")
    guardar_graficas(celdas, tiempos)


if __name__ == "__main__":
    main()
