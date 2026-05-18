*This project has been created as part of the 42 curriculum by pmieres- and lhernan-*

# ⭐▁ ▂ ▃ ▅ ▆ ▇ ▌ A-Maze-Ing ▐ ▇ ▆ ▅ ▃ ▂ ▁⭐

## 📋 Description

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
Elegimos el *Recursive Backtracker* (Búsqueda en Profundidad Aleatorizada).
¿Por qué este algoritmo?

- Produce laberintos estéticamente agradables con pasillos largos y un buen nivel de desafío.
- Es simple de implementar y depurar.
- Ofrece un excelente rendimiento para los tamaños requeridos.
- Garantiza de forma natural un laberinto perfecto (árbol de expansión) cuando `PERFECT=True`.
- Es fácil de adaptar para laberintos no perfectos añadiendo ciclos aleatorios.

## 👥 Equipo y Gestión del Proyecto

- **pmieres-**: Algoritmos de generación de laberintos, lógica central, paquete reutilizable, formato de salida.
- **lhernan-**: Visualización (ASCII + colores), menú interactivo, analizador de configuración (*parser*), manejo de errores, Makefile.

Evolución de la planificación:
Comenzamos con un *backtracker* básico + representación en cuadrícula. Luego separamos el generador en un paquete reutilizable. Finalmente nos enfocamos en la parte visual/interactiva y en los retoques finales.

Qué funcionó bien:
- Separación temprana de conceptos (generador frente a visualización).
- Uso extensivo de pistas de tipo (*type hints*) y pruebas.
- Buen manejo de errores desde el principio.

Qué se podría mejorar:
- Más pruebas unitarias para casos extremos (*edge cases*).
- Animación durante la generación (puntos extra).

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