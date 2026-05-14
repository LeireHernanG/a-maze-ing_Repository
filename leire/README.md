_Este proyecto ha sido creado como parte del currículo de 42 por pmieres- y lhernan-_
# ⭐▁ ▂ ▃ ▅ ▆ ▇ ▌ A-Maze-Ing ▐ ▇ ▆ ▅ ▃ ▂ ▁⭐​
## 📋 Descripción del proyecto

**Push_swap** consiste en ordenar una lista de números enteros utilizando **dos stacks** (`a` y `b`) y un conjunto muy limitado de operaciones. El objetivo es generar la secuencia **más corta posible** de instrucciones para dejar la pila `a` ordenada en orden ascendente (el número más pequeño en la cima).

Características principales del proyecto:

- Múltiples algoritmos con diferentes complejidades: **O(n²)**, **O(n√n)**, **O(n log n)** y uno **adaptativo**
- Selección inteligente del algoritmo según el **grado de desorden** de la entrada
- Sistema de benchmark integrado para medir rendimiento
- Manejo estricto de errores (duplicados, no enteros, overflow, etc.)

## Instructions
### 🚀 Compilación

```bash
make install        # Instala los requisitos necesarios(especificados en "requirements.txt")
make run            # Ejecuta el programa
make debug          # Comienza el debug
make lint           # Cmprueba que las reglas e flake8 y mipy esten correctas
make lint-stric     # ingual que e anterior pero con estricto
make clean          #Limia el pycache
```
```bash
INSTRUCOMANDOS DEL DEBUG
n	        #Next — ejecuta la línea actual y pasa a la siguiente
s	        #Step — entra dentro de una función
c	        #Continue — ejecuta hasta el siguiente breakpoint (o hasta el final)
l	        #List — muestra el código alrededor de donde estás
p variable	#Print — imprime el valor de una variable, ej: p self._estado
b 42	    #Breakpoint — pone un punto de parada en la línea 42
q	        #Quit — sale del debugger
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

## Algoritmos

## Recursos
Referencias
- Google : 
    - Sorting algorithm 
    - Visión general de algoritmos de ordenación.
    - Radix sort explanation 
    - Detalles sobre radix adaptado a stacks.
    - Push_swap tutorial - Guía para implementar en stacks.
 #### Uso de IA

Usamos IA para :
- testers
- En depuración: sugerencias para fixing bugs en rotaciones y indexing.
- No se usó para código principal; revisamos y reescribimos todo manualmente para comprensión total.
- Para el README: IA ayudó a estructurar y redactar secciones, pero contenido basado en nuestro trabajo.

## Prubas para la correcion:
#### Generas la lista una vez
ARG=$(shuf -i 1-200 -n 50 | tr '\n' ' ')
echo $ARG > input.txt

#### Cada prueba usa la misma lista
ARG=$(cat input.txt)
./push_swap $ARG | tee ops.txt | ./checker_linux $ARG
echo "Operaciones usadas:" $(wc -l < ops.txt)