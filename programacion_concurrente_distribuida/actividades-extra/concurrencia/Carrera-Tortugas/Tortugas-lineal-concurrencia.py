import threading
import random
import time

META = 100  # Distancia necesaria para ganar la carrera

# -----------------------------------
# ESTADO COMPARTIDO ENTRE LOS HILOS
# -----------------------------------
tortugas = {
    "Tortuga 1": 0,
    "Tortuga 2": 0,
    "Tortuga 3": 0,
    "Tortuga 4": 0
}

ganador = None            # Se rellenará cuando alguna tortuga llegue a META
carrera_activa = True     # Controla cuándo deben seguir corriendo los hilos
lock = threading.Lock()   # Evita condiciones de carrera al leer/modificar tortugas


# -----------------------------------
# HILO 1: MOVER LAS TORTUGAS
# Este hilo incrementa las posiciones de TODAS las tortugas
# -----------------------------------
def mover_tortugas():
    global carrera_activa, ganador

    # El hilo avanza tortugas continuamente mientras no haya ganador
    while carrera_activa:

        # Bloqueo para modificar el diccionario de manera segura
        lock.acquire()
        try:
            for nombre in tortugas:
                avance = random.randint(1, 10)  # Avance aleatorio por turno
                tortugas[nombre] += avance      # Actualiza posición
        finally:
            lock.release()  # Libera para que otros hilos puedan leer/escribir

        time.sleep(0.3)  # Hace que este hilo avance a un ritmo propio


# -----------------------------------
# HILO 2: MOSTRAR PROGRESO
# Este hilo SOLO imprime el estado actual de la carrera
# -----------------------------------
def mostrar_progreso():
    # Igual que antes: sigue mientras no haya ganador
    while carrera_activa:

        lock.acquire()
        try:
            print("\n--- Estado actual ---")
            for nombre, pos in tortugas.items():
                print(f"{nombre} lleva {pos} metros")
        finally:
            lock.release()

        time.sleep(0.4)  # Ritmo propio de impresión (diferente al movimiento)


# -----------------------------------
# HILO 3: COMPROBAR GANADOR
# Este hilo revisa quién llega primero a META
# -----------------------------------
def comprobar_ganador():
    global carrera_activa, ganador

    while carrera_activa:

        lock.acquire()
        try:
            for nombre, pos in tortugas.items():
                # Si alguna tortuga llega y aún no hay ganador → gana
                if pos >= META and ganador is None:
                    ganador = nombre
                    carrera_activa = False      # Detiene todos los hilos
                    print(f"\n🏁 {ganador} ha ganado la carrera!\n")
        finally:
            lock.release()

        time.sleep(0.1)  # Este hilo revisa con más frecuencia


# -----------------------------------
# CREACIÓN Y EJECUCIÓN DE LOS HILOS
# -----------------------------------
h1 = threading.Thread(target=mover_tortugas)   # Hilo que mueve tortugas
h2 = threading.Thread(target=mostrar_progreso) # Hilo que imprime progreso
h3 = threading.Thread(target=comprobar_ganador) # Hilo que detecta ganador

# Iniciar los hilos
h1.start()
h2.start()
h3.start()

# Esperar a que los 3 hilos terminen antes de cerrar el programa
h1.join()
h2.join()
h3.join()

print("La carrera ha terminado.")
