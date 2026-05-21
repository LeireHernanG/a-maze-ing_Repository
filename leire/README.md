*This project has been created as part of the 42 curriculum by pmieres- and lhernan-*

# ⭐▁ ▂ ▃ ▅ ▆ ▇ ▌ A-Maze-Ing ▐ ▇ ▆ ▅ ▃ ▂ ▁⭐

## 📋 Descripción

**A-Maze-Ing** es un generador de laberintos escrito en Python que crea laberintos personalizables a partir de un archivo de configuración, garantiza una estructura válida (incluyendo el icónico patrón "42") y proporciona tanto una salida de archivo como una representación visual interactiva.

Características clave:
- Generación de laberintos perfectos (camino único) o laberintos con ciclos
- Generación reproducible mediante el uso de semillas (seeds).
- Visualización en terminal mediante arte ASCII con colores.
- Menú interactivo (regenerar, mostrar/ocultar solución, cambiar temas).
- Paquete reutilizable MazeGenerator (mazegen-*).
- Manejo estricto de errores y validación de configuración.

---

## 🚀 Instructions

### Compilation & Execution

```bash
make install        # Instala las dependencias (requirements.txt)
make run            # Ejecuta el programa
make debug          # Inicia una sesión de depuración (pdb)
make lint           # Verifica el código con flake8 + mypy
make lint-strict    # Modo estricto de verificación
make clean          # Limpia __pycache__ y archivos temporales
```
### Debug Commands
```bash
n           #Next — ejecuta la línea actual y pasa a la siguiente
s           #Step — entra dentro de una función
c           #Continue — ejecuta hasta el siguiente breakpoint (o hasta el final)
l           #List — muestra el código alrededor de donde estás
p variable  #Print — imprime el valor de una variable, ej: p self._estado
b 42        #Breakpoint — pone un punto de parada en la línea 42
q           #Quit — sale del debugger
```

## CONFIGURACIÓN

El archivo de configuración (`config.txt`) sigue el formato `KEY=VALUE`, una por línea. Las líneas que empiezan por `#` son comentarios y se ignoran.

### Mandatory keys

| Key | Description | Example |
| :--- | :--- | :--- |
| `WIDTH` | Ancho del laberinto en celdas | `WIDTH=25` |
| `HEIGHT` | Alto del laberinto en celdas | `HEIGHT=15` |
| `ENTRY` | Coordenadas de entrada (x,y) | `ENTRY=1,0` |
| `EXIT` | Coordenadas de salida (x,y) | `EXIT=14,3` |
| `OUTPUT_FILE` | Archivo donde se guarda el laberinto | `OUTPUT_FILE=laberinto.txt` |
| `PERFECT` | `True` para laberinto perfecto, `False` para permitir ciclos | `PERFECT=True` |
### Ejecución

- Uso básico:
            
            make run


A continuación te mostrara el laberinto y un menu:
```bash
            ¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤                                  
            ║                       ║           ║     O ║           ║           ║                                  
            ¤   ¤   ¤═══¤═══¤═══¤   ¤   ¤═══¤   ¤   ¤═══¤   ¤═══¤   ¤   ¤═══¤   ¤                                  
            ║   ║   ║           ║   ║   ║       ║       ║   ║   ║       ║   ║   ║                                  
            ¤═══¤   ¤   ¤   ¤═══¤   ¤   ¤   ¤═══¤═══¤   ¤   ¤   ¤═══¤═══¤   ¤   ¤                                  
            ║     X     ║       ║   ║   ║   ║       ║       ║   ║           ║   ║                                  
            ¤   ¤   ¤═══¤═══¤   ¤   ¤   ¤═══¤   ¤   ¤═══¤═══¤   ¤   ¤═══¤   ¤   ¤                                  
            ║   ║   ║       ║           ║                       ║       ║       ║                                  
            ¤   ¤═══¤   ¤   ¤═══¤   ¤═══¤   ¤═══¤   ¤   ¤═══¤═══¤═══¤   ¤═══¤═══¤                                  
            ║           ║       ║   ║       ║       ║               ║   ║       ║                                  
            ¤   ¤═══¤═══¤═══¤   ¤   ¤   ¤═══¤   ¤   ¤═══¤═══¤   ¤   ¤   ¤═══¤   ¤                                  
            ║   ║   ║           ║   ║       ║   ║           ║       ║   ║       ║                                  
            ¤   ¤   ¤   ¤═══¤═══¤═══¤═══¤   ¤   ¤═══¤═══¤═══¤   ¤═══¤   ¤   ¤   ¤                                  
            ║   ║               ║   ║   ║   ║   ║   ║   ║   ║       ║       ║   ║                                  
            ¤   ¤   ¤═══¤═══¤   ¤═══¤   ¤   ¤   ¤═══¤═══¤═══¤═══¤   ¤═══¤═══¤   ¤                                  
            ║           ║   ║   ║   ║                   ║   ║   ║               ║                                  
            ¤═══¤═══¤   ¤   ¤   ¤═══¤═══¤═══¤   ¤═══¤═══¤═══¤   ¤═══¤═══¤═══¤═══¤                                  
            ║       ║       ║   ║   ║   ║   ║   ║   ║   ║   ║       ║           ║                                  
            ¤   ¤   ¤═══¤   ¤   ¤═══¤═══¤═══¤   ¤═══¤═══¤═══¤   ¤   ¤   ¤   ¤   ¤                                  
            ║   ║       ║   ║           ║   ║   ║   ║           ║           ║   ║                                  
            ¤   ¤═══¤   ¤   ¤═══¤═══¤   ¤═══¤   ¤═══¤═══¤═══¤   ¤═══¤   ¤═══¤   ¤                                  
            ║       ║   ║           ║   ║   ║   ║   ║   ║   ║       ║           ║                                  
            ¤═══¤   ¤   ¤═══¤   ¤   ¤   ¤═══¤   ¤═══¤═══¤═══¤   ¤   ¤   ¤   ¤   ¤                                  
            ║       ║           ║   ║   ║       ║               ║   ║   ║   ║   ║                                  
            ¤   ¤═══¤═══¤═══¤   ¤   ¤   ¤   ¤═══¤   ¤═══¤═══¤═══¤   ¤   ¤═══¤   ¤                                  
            ║   ║           ║   ║   ║   ║       ║   ║               ║       ║   ║                                  
            ¤   ¤═══¤═══¤   ¤   ¤   ¤   ¤═══¤   ¤   ¤   ¤═══¤═══¤═══¤═══¤   ¤   ¤                                  
            ║   ║       ║   ║       ║       ║   ║   ║   ║       ║           ║   ║                                  
            ¤   ¤   ¤   ¤   ¤═══¤═══¤   ¤   ¤   ¤   ¤   ¤   ¤═══¤   ¤   ¤═══¤   ¤                                  
            ║       ║   ║           ║   ║   ║   ║   ║   ║   ║       ║           ║                                  
            ¤   ¤   ¤   ¤   ¤═══¤   ¤   ¤═══¤   ¤═══¤   ¤   ¤   ¤═══¤═══¤═══¤═══¤                                  
            ║       ║       ║       ║                   ║                       ║                                  
            ¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤═══¤                                  

⭐▁ ▂ ▃ ▅ ▆ ▇ ▌ A-Maze-Ing ▐ ▇ ▆ ▅ ▃ ▂ ▁⭐​

1. Regenerate a new maze 🔄​
2. Show/Hide path from entry to exit ​👁️‍🗨️​
3. Rotate maze colors​ 🔴​🟢​🔵​
4. Quit ​⛔​

-Select an option? (1-4):
```
- Selectores opcionales:
    1. **Regenerate a new maze 🔄​**: Generara un nuevo laberinto
    2. **Show/Hide path from entry to exit ​👁️‍🗨️**: Mostrara la scuencia hacia la salida sin mostrar el menu
    3. **Rotate maze colors​ 🔴​🟢​🔵​**: Te ofrecera tres opciones de paletas
    4. **Quit ​⛔​**: Sale del programa
```bash
            === Rotate maze colors ===
            1. Mario bros
            2. Space
            3. Hot pink
            Choose theme:
```


- El tamaño del laberinto se puede cambiar con el archivo "config.txt" se deberan de meter los datos de forma correcta: **KEY=VALUE** 
```bash

### EJEMPLO

WIDTH=17
HEIGHT=16
ENTRY=10,0
EXIT=1,2
OUTPUT_FILE=laberinto.txt
PERFECT=False
SEED=42

### Para verificar

En caso de error saltara un aviso:
    HEIGHT=a
    Couldn't make the maze:The parameter 'HEIGHT' must an Integer
```
## Algoritmo de Generación de Laberintos
Elegimos el *DFS Depht-Firt Search*.
¿Por qué este algoritmo?

- Produce laberintos estéticamente agradables con pasillos largos y un buen nivel de desafío.
- Es simple de implementar y depurar.
- Ofrece un excelente rendimiento para los tamaños requeridos.
- Garantiza de forma natural un laberinto perfecto cuando `PERFECT=True`.
- Es fácil de adaptar para laberintos no perfectos añadiendo ciclos aleatorios.
## INSTALACIÓN DE MODULO MAZEGENERATOR
# mazegen

A reusable Python package for maze generation and solving.

---

## Installation

Build and install the package:

```bash
pip install build
python -m build
pip install dist/mazegen-0.1.0-py3-none-any.whl
```

You can also install the source archive:

```bash
pip install dist/mazegen-1.0.0.tar.gz
```

---

## Basic Usage

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
		width=5,
		height=5,
		entry=(0, 0),
		exit=(3, 3),
		perfect=False
)

maze.gen_maze()

print(maze.structure())
```

---

## Custom Parameters

The generator accepts custom parameters such as seed.

Example:

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
		width=5,
		height=5,
		entry=(0, 0),
		exit=(3, 3),
		perfect=False,
		seed=123
)

maze.generate()
```

### Parameters

* `width` (`int`) :
  Width of the maze.

* `height` (`int`) :
  Height of the maze.

* `entry` (`tuple[int, int]`) :
  Entry point coordinates (x, y).

* `exit` (`tuple[int, int]`) :
  Exit point coordinates (x, y).

* `perfect` (`bool`) :
  If True, generates a perfect maze (one solution).

* `seed` (`int`, optional) :
  Random seed used to generate reproducible mazes.

---

## Accessing the Maze Structure

The generated maze structure can be accessed directly from the generator.

Example:

```python
structure = maze.structure

print(structure)
```
---

## Accessing a Maze Solution

The module also provides the  shortest solution path.

Example:

```python
solution = maze.solution

# Shortest solution
print(solution)
```

The solution is returned as a sequence of coordinates representing a valid path from the maze entrance to the exit.

---

## Example

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
		width=5,
		height=5,
		entry=(0, 0),
		exit=(3, 3),
		perfect=False,
		seed=123
)

maze.gen_maze()

print("Maze structure:")
print(maze.structure)

print("Maze solution:")
print(maze.solution[0])
```

---

## Package Structure

```text
mazegen/
├── __init__.py
└── generator.py
```

Main class:

* `MazeGenerator`

---

## Build Instructions

To rebuild the package from source:

```bash
python -m pip install --upgrade build
python -m build
```

Generated files will be available inside the `dist/` directory.

Example:

```text
dist/
├── mazegen-1.0.0.tar.gz
└── mazegen-1.0.0-py3-none-any.whl
```


## 👥 Equipo y Gestión del Proyecto

- **pmieres-**: Algoritmos de generación de laberintos, paquete reutilizable, parser y manejo de errores
- **lhernan-**: Visualización (ASCII + colores), menú interactivo,formato de salida y Makefile.

Evolución de la planificación:
Comenzamos con el algoritmo basico + representación en cuadrícula. Luego separamos el generador en un paquete reutilizable. Finalmente nos enfocamos en la parte visual/interactiva y en los retoques finales.

Qué funcionó bien:
- Separación temprana de conceptos (generador frente a visualización).
- Uso extensivo de pistas de tipo (*type hints*) y pruebas.
- Buen manejo de errores desde el principio.

Herramientas utilizadas:
- Python 3.11, flake8, mypy, pytest
- Git + GitHub
- IA (ver más abajo)

## Recursos
Referencias:
- Explicaciones e implementaciones de *Recursive Backtracker*.
- Documentación de la asignatura de 42.
- Foros y vídeos.

#### Uso de IA

Usamos IA para:
- Creación de pruebas (*testers*).
- En depuración: sugerencias para solucionar errores (*bugs*) en las rotaciones y en la indexación.
- No se usó para el código principal; revisamos y reescribimos todo manualmente para lograr una comprensión total.
- Para el README: la IA ayudó a estructurar y redactar secciones, pero el contenido está basado en nuestro trabajo.