"""Desarrolla un administrador de tareas para un sistema operativo. 
Los procesos (tareas) se ejecutan de manera concurrente, y el administrador debe coordinar la ejecución de las tareas. 
Utiliza una cola (queue) para gestionar la ejecución de las tareas.

En este ejercicio, debes implementar las siguientes funciones:
1. **agregar_tarea(nombre, duracion)**: 
- Esta función agrega una nueva tarea a la cola de tareas pendientes. 
- Debes especificar el nombre de la tarea y su duración estimada en segundos.

2. **ejecutar_tarea()**: 
- Esta función toma la tarea de mayor prioridad (aquella con la duración más corta) de 
  la cola de tareas pendientes y la ejecuta.
- Debes simular la ejecución de la tarea mediante un retraso de la duración especificada.

3. **mostrar_tareas_pendientes()**: 
- Esta función muestra la lista de tareas pendientes en la cola.

4. **mostrar_tareas_completadas()**: 
- Esta función muestra la lista de tareas que han sido ejecutadas.

Utiliza una cola para gestionar las tareas pendientes y asegurarte de que las tareas se 
ejecuten en el orden correcto, es decir, primero las tareas más cortas.
"""

import threading
import time
import queue

#Cola para gestionar las tareas pendientes
cola_tareas = queue.PriorityQueue()  #se utiliza PriorityQueue para la tarea de menor duración
tareas_completadas = []  #lista para almacenar las tareas completadas
mutex = threading.Lock()  #mutex para proteger el acceso a la cola de tareas
semaforo = threading.Semaphore(0)  #semaforo para coordinar la ejecución de las tareas
ejecutando = True  #variable para controlar la ejecución del hilo

def agregar_tarea(nombre, duracion):
    """Agrega una nueva tarea a la cola de tareas pendientes."""
    cola_tareas.put((duracion, nombre))  #la cola usa la duración como prioridad
    print("\nTarea agregada: '" + nombre + "' con duración " + str(duracion) + " segundos.")
    semaforo.release()  #señala que hay una tarea disponible

def ejecutar_tarea():
    """Ejecuta la tarea de mayor prioridad (menor duración) de la cola."""
    while ejecutando or not cola_tareas.empty():  #continua hasta que se indique que no se ejecuta
        semaforo.acquire()  #espera hasta que haya una tarea disponible
        mutex.acquire()  #adquiere el mutex para acceso seguro a la cola
        if not cola_tareas.empty():
            duracion, nombre = cola_tareas.get()  #toma la tarea con menor duración
            mutex.release()  #libera el mutex después de tomar la tarea

            #Simula la ejecución de la tarea
            print("\nEjecutando tarea: '" + nombre + "' durante " + str(duracion) + " segundos...")
            time.sleep(duracion)  #retraso por la duración de la tarea
            print("Tarea completada: '" + nombre + "'")

            #Agrega la tarea a la lista de completadas
            tareas_completadas.append(nombre)
        else:
            mutex.release()  #libera el mutex si no hay tareas

def mostrar_tareas_pendientes():
    """Muestra la lista de tareas pendientes."""
    if cola_tareas.empty():
        print("No hay tareas pendientes.")
    else:
        print("\nTareas pendientes:")
        for duracion, nombre in list(cola_tareas.queue):
            print(" - '" + nombre + "' (Duración: " + str(duracion) + " segundos)")

def mostrar_tareas_completadas():
    """Muestra la lista de tareas que han sido ejecutadas."""
    if not tareas_completadas:
        print("No hay tareas completadas.")
    else:
        print("\nTareas completadas:")
        for nombre in tareas_completadas:
            print(" - '" + nombre + "'")

#Crea y lanza el hilo para ejecutar tareas
hilo_ejecutor = threading.Thread(target=ejecutar_tarea)
hilo_ejecutor.start()

#Ejemplo de uso
agregar_tarea("Tarea 1", 5)
agregar_tarea("Tarea 2", 2)
agregar_tarea("Tarea 3", 1)

#Muestra tareas pendientes
mostrar_tareas_pendientes()

#Espera un momento para dar tiempo a la ejecución
time.sleep(3)

#Mostra tareas completadas
mostrar_tareas_completadas()

#Finaliza el hilo de ejecución
ejecutando = False  #cambia la variable para detener el hilo de ejecución
semaforo.release()  #libera el semáforo para que el hilo pueda salir del bucle
hilo_ejecutor.join()  #espera a que el hilo termine
print("\nTodas las tareas han sido ejecutadas y el hilo ha finalizado.")
