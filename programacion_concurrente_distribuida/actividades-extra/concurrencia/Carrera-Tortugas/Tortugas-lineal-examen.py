import random
import time

# Diccionario donde cada clave es una tortuga y su valor es la posición actual.
tortugas = {
    "Tortuga 1": 0,
    "Tortuga 2": 0,
    "Tortuga 3": 0,
    "Tortuga 4": 0
}

meta = 100               # Distancia que deben alcanzar para ganar
ganador = None           # Se guarda el ganador cuando ocurra
carrera_en_curso = True  # Controla si seguir o detener el bucle principal

# ----------------------------
#   CARRERA LINEAL
# ----------------------------
while carrera_en_curso:

    print("\n--- Nuevo turno ---")

    # Cada tortuga avanza una vez en cada turno (todo ocurre en orden)
    for nombre in tortugas:

        # Velocidad aleatoria que cambia cada turno
        velocidad = random.randint(1, 10)

        # Actualizar la posición de la tortuga
        tortugas[nombre] = tortugas[nombre] + velocidad

        # Mostrar avance
        print(nombre, "lleva", tortugas[nombre], "metros")

        # Comprobar si la tortuga llegó a la meta
        if tortugas[nombre] >= meta and ganador is None:
            ganador = nombre
            carrera_en_curso = False
            print("\n🏁", ganador, "ha ganado la carrera!\n")

    time.sleep(0.5)  # Pausa corta para simular tiempo de carrera

print("La carrera ha terminado")
