"""SEMAFORO SIMPLE"""
# Escribir el código de un programa “Semaforo Simple”, el cual es un simulador de un cruce con un semáforo:
# 1. Se creará una función generadora que creará inicialmente 5 coches. Cada coche va a estar compuesto por un array con [nombre,
# velocidad, vueltas] (velocidad y vueltas no se usará por ahora. Se pueden inicializar a 0).
# 2. Mediante colas, se crearán dos tramos, un tramoA para el espacio inicial donde estarán los coches esperando a que se abra el
# semáforo, y un tramo Cruce, para el espacio a dónde van los coches al cruzar el semáforo.
# 3. Se creará una función para, cada cierto tiempo (i.e.: 2 seg) pintar por pantalla el cruce y los coches presentes en cada uno de los
# tramos.
# 4. Se crearán una serie de hilos para la función de cruzar para “hacer ir” a los coches del tramoA al Cruce (progresiva y aleatoriamente,
# mediante un sleep random) y un único hilo para la función de pintar el cruce. Cuando un coche no pueda cruzar, se quedará en el
# tramo original en su posición y se escribirá un mensaje por pantalla indicando que no ha podido cruzar.
# 5. Se implementará un semáforo para controlar el paso de los coches del tramoA hacia el cruce. La función de pintar deberá parar todos los
# cruces y tomar el control absoluto de la pantalla para pintar el cruce.
# El resultado específico puede variar en cada ejecución debido a la aleatoriedad en la velocidad de los vehículos en cruzar.

import threading
import queue
import random
import time

# Función para generar coches
def generar_coches():
    coches = []
    for i in range(5):
        nombre = f"Coche_{i+1}"
        velocidad = 0  # No se usa por ahora
        vueltas = 0    # No se usa por ahora
        coche = [nombre, velocidad, vueltas]
        coches.append(coche)
    return coches

# Función que controla el cruce de coches
def cruzar_coche(tramoA, cruce, semaforo, mutex_pintar):
    while not tramoA.empty():
        coche = tramoA.get()  # Extraer un coche del tramoA
        
        # Intentar cruzar si el semáforo lo permite
        semaforo.acquire()  # Espera a que el semáforo esté en verde
                
        with mutex_pintar:  # Proteger la salida por pantalla
            print(f"{coche[0]} está cruzando el semáforo...")

        time.sleep(random.uniform(1, 3))  # Simular el tiempo de cruce (aleatorio)

        with mutex_pintar:
            print(f"{coche[0]} ha cruzado y está en el cruce.")

        cruce.put(coche)  # Colocar el coche en el cruce
        semaforo.release()  # Permitir el siguiente coche

# Función para pintar el estado de los tramos
def pintar_estado(tramoA, cruce, mutex_pintar):
    while not tramoA.empty() or not cruce.empty():
        with mutex_pintar:  # Proteger la salida por pantalla
            print("\nEstado actual:")
            print("TramoA:", list(tramoA.queue))
            print("Cruce:", list(cruce.queue))
        time.sleep(2)  # Pintar cada 2 segundos

# Función principal
def semaforo_simple():
    # Crear la cola para el tramoA y cruce
    tramo_a = queue.Queue()
    cruce = queue.Queue()
    
    # Generar coches
    coches = generar_coches()
    
    # Meter coches al tramoA
    for coche in coches:
        tramo_a.put(coche)
    
    # Crear semáforo con capacidad de 1 (solo un coche puede cruzar a la vez)
    semaforo = threading.Semaphore(1)
    
    # Mutex para proteger el acceso a la pantalla
    mutex_pintar = threading.Lock()
    
    # Crear y lanzar el hilo para pintar el estado de los tramos
    hilo_pintar = threading.Thread(target=pintar_estado, args=(tramo_a, cruce, mutex_pintar))
    hilo_pintar.start()
    
    # Crear y lanzar hilos para cruzar coches
    hilos_cruzar = []
    for _ in range(5):
        hilo = threading.Thread(target=cruzar_coche, args=(tramo_a, cruce, semaforo, mutex_pintar))
        hilos_cruzar.append(hilo)
        hilo.start()

    # Esperar a que todos los coches crucen
    for hilo in hilos_cruzar:
        hilo.join()

    # Esperar a que el hilo de pintar termine
    hilo_pintar.join()

# Ejecutar el programa
if __name__ == "__main__":
    semaforo_simple()
