# Tarea 1 - Juego de la Vida de Conway
## Esteban Ramirez
IIC2026 - G1 - Computación Paralela y Distribuida

## Requisitos
Las librerias requeridas estan en `requirements.txt`.
- Python 3.10+
- `numpy`
- `matplotlib`

## Estructura del proyecto

```text
📁 Tarea1/
├── 📄 game_of_life.py      # Clase principal y reglas del juego
├── 📄 visualizer.py        # Genera animaciones GIF
├── 📄 benchmark.py         # Mide tiempos y genera graficas
├── 📄 requirements.txt     # Dependencias del proyecto
├── 📄 README.md            # Explicacion y uso del proyecto
└── 📁 outputs/             # Imagenes y GIFs generados
```
## Instalacion y uso
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Empezar a usar
Desde la terminal puede ejecutar `python` y pegar los siguientes comandos:

```python
from game_of_life import GameOfLife

juego = GameOfLife(32, 32)
juego.run(10)
tablero = juego.get_state()
```
La parte `juego = GameOfLife(32, 32)` representa el tamaño del tablero de 32x32, estos valores se pueden personalizar.

Tambien hay patrones iniciales predefinidos:

```python
glider = GameOfLife.glider()
blinker = GameOfLife.blinker()
toad = GameOfLife.toad()
```

### Generar animaciones

Ejecutar

```powershell
python visualizer.py
```

Esto crea estos GIFs ubicados en:

- `outputs/glider_32.gif`
- `outputs/blinker_32.gif`
- `outputs/random_128.gif`

#### Generar animaciones con tableros de hasta 512
Dentro de la terminal ejecuta `python` y luego pega el siguiente comando:
```python
from visualizer import animate_game

animate_game("random", 32, 50)
```
Donde `animate_game("random", 32, 50)` representa:
- El patrón es aleatorio (valores disponibles: random, glider, blinker, toad)
- Dimension de `32x32`
- Cantidad de generaciones `50`

Ejemplo:
![](./outputs/random_128.gif)

### Ejecutar el benchmark

Ejecutar

```powershell
python benchmark.py
```

El benchmark prueba tableros de `32, 64, 128, 256, 512 y 1024`.
Para cada tamano ejecuta 10 generaciones y muestra el tiempo promedio por
generacion.
Los resultados se pueden ver en la ruta:

- `outputs/benchmark_linear.png`
- `outputs/benchmark_loglog.png`

![Benckmark Log-log](./outputs/benchmark_loglog.png)