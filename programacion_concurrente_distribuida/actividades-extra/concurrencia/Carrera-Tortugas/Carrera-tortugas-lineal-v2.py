import random
import time
#CODIO ESTUDIAR
## ----------------------------------------------------
##  PROGRAMA LINEAL "CARRERA DE TORTUGAS"
##  - Todas las tortugas avanzan en el MISMO hilo
##  - Todo ocurre de forma ORDENADA y SECUENCIAL
##  - Esta es la versión base antes de pasar a concurrencia
## ----------------------------------------------------

# Diccionario donde cada clave es el nombre de una tortuga
# y el valor es la distancia recorrida hasta el momento.
tortugas = {
    "tortuga_1": 0,
    "tortuga_2": 0,
    "tortuga_3": 0,
    "tortuga_4": 0
}

meta = 100                 # Distancia para ganar la carrera
ganador = None             # Se guardará el nombre de la tortuga ganadora
carrera_en_curso = True    # Controla si la carrera continúa o termina


## ----------------------------------------------------
##  BUCLE PRINCIPAL DE LA CARRERA (VERSIÓN LINEAL)
## ----------------------------------------------------
# Mientras la carrera esté activa, este bucle sigue ejecutándose.
# Todo sucede en un único hilo, de forma ordenada.
while carrera_en_curso:

    # Recorremos todas las tortugas una por una (orden fijo)
    for nombre in tortugas:

        # Avance aleatorio entre 1 y 10 metros
        avance = random.randint(1, 10)

        # Actualizamos la posición de esta tortuga
        tortugas[nombre] += avance

        # Mostramos su progreso
        print(f"{nombre} lleva {tortugas[nombre]} metros")

        # Pausa para simular el tiempo entre movimientos
        # (hace la carrera más “real”, pero sigue siendo lineal)
        time.sleep(0.2)

        # Comprobamos si esta tortuga ha llegado a la meta
        # El ganador solo se establece UNA vez
        if tortugas[nombre] >= meta and ganador is None:
            ganador = nombre
            carrera_en_curso = False   # Detenemos la carrera
            print(f"\n🏁  {ganador} ha ganado la carrera\n")

# Cuando salimos del while, la carrera terminó
print("La carrera ha terminado")
